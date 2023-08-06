import numpy as np
import pickle
import os
import math
import sys
import warnings
import logging
import time
import hs_bridge.wrapped_dmadump.dmadump as dmadump
from hs_bridge.config import *

def text2script(cmd_str):
    """Converts a string of hex characters into the correct format to suppyl to the adxdma dump command.

    Given a string of hex characters with the left most character containing the MSB create a string of pairs of hex characters representing bytes
    with the leftmost byte contanining the LSB in the format expected by the adxdma_dmadump binary for the data argument.

    Parameters
    ----------
    cmd_str : str
        The string of hexidecimal characters to format. The first character represents the hex character containing the MSB

    Returns
    -------
    script_txt : str
        The formated string of bytes
    """
    cmd = cmd_str
    script_txt = ''
    while cmd:
        script_txt += '0x' + cmd[-2:] + ' '
        cmd = cmd[0:-2]
    return script_txt


class fpga_compiler:
    """Produces the needed adxdma dump scripts of a given network to program HBM

    Attributes
    ----------
    input : dict
        The inputs to the network for each timestep. Key, timestep value, list of axons
    axon_ptrs : numpy array
        Array of tuples pointing to the rows containing the synapses for the corresponding Axon.
    Each tuple is (start row, end row).
    neuron_ptrs : numpy array
        Array of tuples pointing to the rows containing the synapses for the corresponding Axon.
    Each tuple is (start row, end row).
    synapses : list
        List of tuples corresponding to synapses. Each tuple is (oncore/offcore bit, synapse address (row index of destination neuron pointer in HBM calculated as floor(destination neuron index / number of neuron groups)), weight)
    HBM_WRITE_CMD : str

    HBM_OP_RW  : str
        OP code to read/write to hbm vie PCie
    NRN_BASE_ADDR : int
        Starting address of neuron pointers in HBM
    SYN_BASE_ADDR : int
        Starting address of synapses in HBM
    PTR_ADDR_BITS : int
        Number of bits used to represent pointer starting adderess
    PTR_LEN_BITS :
        Number of bits used to represent the number of rows of synapses a pointer corresponds to
    SYN_OP_BITS :
        Number of bits used to represent synapse opcode
    SYN_ADDR_BITS :
        Number of bits used to represent synapse address
    SYN_WEIGHT_BITS :
        Number of bits used to represent synapse weight

    """


    # OP code to read/write to hbm vie PCie
    #HBM_OP_RW = '02' + 28 * '00'

    #TODO: these values should be in the config.py file
    #PTR_ADDR_BITS = 23  # HBM row address
    #PTR_LEN_BITS = 9  # (8 connections/row x 2^9 rows = 2^12 = 4K connections max)
    #AXN_BASE_ADDR = 0  # axon pointer start address
    ##NRN_BASE_ADDR = 2 ** 14  #commented out, this value lives in config.py. neuron pointer start address (2^17 axons / 8 axon pointers/row = 2^14 rows max)
    #SYN_BASE_ADDR = 2 ** 15  # (2^17 neurons / 8 neuron pointers/row = 2^14 rows max -> 2^14+2^14=2^15)

    #SYN_ADDR_BITS = 13  # each synapse: [31:29]=OpCode  [28:16]=address, [15:0]=weight (1 sign + 15 value, fixed-point)
    #SYN_WEIGHT_BITS = 16
    #SYN_OP_BITS = 3

    #HBM_WRITE_CMD = 'sudo adxdma_dmadump wb 0 0 '

    #WRITE = '01' + 63 * '00'

    def __init__(self, data, N_neurons,  outputs, coreID = 0):
        '''
        Creates the FPGA Compiler object. Populates spike packets in synapses.

        Paramaters
        ----------
        data: list
            Takes the following format: [0]=input data, [1]=axon pointers, [2]=neuron pointers, [3]=synapses
        N_neurons : int
            Number of neurons in network
        CoreID : int
            Index of core in FPGA to write to
        '''
        coreBits = np.binary_repr(coreID,5)+3*'0'#5 bits for coreID
        coreByte = '{:0{width}x}'.format(int(coreBits, 2), width=2)
        self.HBM_OP_RW = '02' + coreByte + 27 * '00'
        self.HBM_OP_RW_LIST = [2,int(coreBits,2)] + [0]*27
        #self.input = data[0]
        self.axon_ptrs = data[0]
        self.neuron_ptrs = data[1]
        self.synapses = data[2]

        n = 0
        errors = 0
        #This works because of how python handles references but it would be much clearer
        #to directly work with self.neuron_ptrs and self.synapses
        #Find space to insert spike packets and insert them in the numpy array representing synapses
        #only assign spike entries in HBM for neurons in the outputs list
        #for row in range(len(data[1])):
            #for col in range(len(data[1][row]))
        rowLength = len(data[1][0])
        for neuronIdx in outputs:
            row = int(np.floor(neuronIdx / rowLength))
            col = neuronIdx % rowLength
            start = data[1][row][col][0]
            end = data[1][row][col][1] + 1
            finished = False
            for r in data[2][start:end]:
                for i in range(len(r)):
                    if r[i] == (0, 0, 0) and n <= len(outputs):
                        r[i] = (1, neuronIdx)
                        #n += 1
                        finished = True
                        break

                if finished:
                    break
            if not finished:
                if n == len(outputs):
                    pass
                else:
                    
                    if n > N_neurons:
                        logging.info('neuron pointer index is greater than specified number of internal neurons, a spike entry will not be assigned to remaining neuron pointer')
                    else:

                         errors+=1
                         logging.error('neuron pointer index: '+ str(n) +' could not be assigned a spike entry')



        logging.info('spike entry assignment errors: ', errors)




    def create_axon_ptrs(self, simDump = False):
        '''
        Creates the necessary adxdma_dump commands to program the axon pointers into HBM

        Returns
        -------
        script : str
            The bash commands to run to program the axon pointers in HBM
        '''

        if simDump:
            dump = []
        axn_ptrs = np.fliplr(self.axon_ptrs)
        batchCmd = []
        for r, d in enumerate(axn_ptrs):

            oldCmd = ''
            cmd = []
            for p in d:
                binAddr = np.binary_repr(p[1] - p[0], PTR_LEN_BITS) + np.binary_repr(p[0] + SYN_BASE_ADDR,
                                                                                    PTR_ADDR_BITS)
                oldCmd += '{:0{width}x}'.format(int(binAddr,2), width=8)
                cmd = cmd + [int(binAddr[:8],2),int(binAddr[8:16],2),int(binAddr[16:24],2),int(binAddr[24:],2)]

            # append HBM write opcode and WRITE command
            oldCmd = self.HBM_OP_RW + '{:0{width}x}'.format(0x800000 + r, width=6) + oldCmd
            rowAddress = '1'+np.binary_repr(r+AXN_BASE_ADDR,23)
            cmd = self.HBM_OP_RW_LIST + [int(rowAddress[:8],2),int(rowAddress[8:16],2),int(rowAddress[16:],2)]  + cmd
            oldCmd = self.txt2script(oldCmd)
            cmd.reverse()
            if simDump:
                dumpCmd = ['{:0{width}x}'.format(i, width=2) for i in cmd]
                dumpCmd.reverse()
                dumpCmd = ''.join(dumpCmd)
                dump.append(dumpCmd)
            else:
                batchCmd = batchCmd + cmd
                #print(cmd)
        if simDump:
            return dump
        else:
            #print(np.array(batchCmd))
            exitCode = dmadump.dma_dump_write(np.array(batchCmd), len(batchCmd), 1, 0, 0, 0, dmadump.DmaMethodNormal)
            

    def txt2script(self, cmd_str):
        """Converts a string of hex characters into the correct format to suppyl to the adxdma dump command.

        Given a string of hex characters with the left most character containing the MSB create a string of pairs of hex characters representing bytes
        with the leftmost byte contanining the LSB in the format expected by the adxdma_dmadump binary for the data argument.

        Parameters
        ----------
        cmd_str : str
            The string of hexidecimal characters to format. The first character represents the hex character containing the MSB

        Returns
        -------
        script_txt : str
            The formated string of bytes
        """
        cmd = cmd_str
        script_txt = ''
        while cmd:
            script_txt += '0x' + cmd[-2:] + ' '
            cmd = cmd[0:-2]
        return script_txt

    def create_neuron_ptrs(self, simDump = False):
        '''
        Creates the necessary data arguments to pass to the adxdma_dump commands to program the neuron pointers into HBM.
        Data arguments for multiple adxdma_dump commands are seperated by new line characters

        Returns
        -------
        script : str
            The data arguments to provide to a series of adxdma_dump commands. Data arguments for successive adxdma_dump commands
        are seperated by newline characters
        '''
        if simDump:
            dump = []
        nrn_ptrs = np.fliplr(self.neuron_ptrs)
        batchCmd = []
        for r, d in enumerate(nrn_ptrs):
            oldCmd = ''
            cmd = []
            for p in d:

                binCmd = np.binary_repr(p[1] - p[0], PTR_LEN_BITS) + np.binary_repr(p[0] + SYN_BASE_ADDR, PTR_ADDR_BITS)
                cmd = cmd + [int(binCmd[:8],2),int(binCmd[8:16],2),int(binCmd[16:24],2),int(binCmd[24:],2)]
                oldCmd += '{:0{width}x}'.format(int(binCmd, 2), width=8)


            # append HBM write opcode and address
            oldCmd = self.HBM_OP_RW + '{:0{width}x}'.format(0x800000 + NRN_BASE_ADDR + r, width=6) + oldCmd
            rowAddress = '1'+np.binary_repr(r+NRN_BASE_ADDR,23)
            cmd = self.HBM_OP_RW_LIST + [int(rowAddress[:8],2),int(rowAddress[8:16],2),int(rowAddress[16:],2)]  + cmd
            oldCmd = self.txt2script(oldCmd) + '\n'
            cmd.reverse()
            if simDump:
                dumpCmd = ['{:0{width}x}'.format(i, width=2) for i in cmd]
                dumpCmd.reverse()
                dumpCmd = ''.join(dumpCmd)
                dump.append(dumpCmd)
            else:
                batchCmd = batchCmd + cmd
                #print(cmd)
        #print(np.array(batchCmd))
        if simDump:
            return dump
        else:
            dmadump.dma_dump_write(np.array(batchCmd), len(batchCmd), 1, 0, 0, 0, dmadump.DmaMethodNormal) 
            #return script

    def create_synapses(self, simDump = False):
        '''
        Creates the necessary adxdma_dump commands to program the synapses into HBM

        Returns
        -------
        script : str
            The bash commands to run to program the synapses in HBM
        '''
        if simDump:
            dump = []
        weights = self.synapses
        #script = ''
        n = 0
        #batchCmd = []
        bigCmdList = []
        for r, d in enumerate(weights):
            oldCmd = ''
            cmd = []
            for w in d:
                if w[0] == 0:
                    # [31] = 0 for internal connections and 1 for external connections, [30:29] = unused for single core
                    # TODO: how do I know if a given synapse is an internal or external connection?
                    binCmd = np.binary_repr( 0, SYN_OP_BITS) + np.binary_repr(int(w[1]), SYN_ADDR_BITS) + np.binary_repr(int(w[2]),SYN_WEIGHT_BITS)
                    oldCmd += '{:0{width}x}'.format(int(binCmd, 2),width=8)
                    cmd = cmd + [int(binCmd[:8],2),int(binCmd[8:16],2),int(binCmd[16:24],2),int(binCmd[24:],2)]
                #TODO: looks like this format is out of date, it should be the same as the above format. It may not be hyper critical
                elif w[0] == 1:
                    #spike = str(w[0]) + 15 * '0'
                    spike = 16 * '0'
                    addr = np.binary_repr(w[1], SYN_ADDR_BITS)
                    #cmd += '{:0{width}x}'.format(int(spike + addr, 2), width=8)
                    binSpike = np.binary_repr( 4, SYN_OP_BITS) + 12*'0' + np.binary_repr(w[1],17)
                    oldCmd += '{:0{width}x}'.format(int(binSpike, 2),width=8)
                    cmd = cmd + [int(binSpike[:8],2),int(binSpike[8:16],2),int(binSpike[16:24],2),int(binSpike[24:],2)]



            # append HBM write opcode and address
            oldCmd = self.HBM_OP_RW + '{:0{width}x}'.format(0x800000 + SYN_BASE_ADDR + r, width=6) + oldCmd
            rowAddress = '1'+np.binary_repr(r+SYN_BASE_ADDR,23)
            cmd = self.HBM_OP_RW_LIST + [int(rowAddress[:8],2),int(rowAddress[8:16],2),int(rowAddress[16:],2)]  + cmd
            oldCmd = self.txt2script(oldCmd) + '\n'
            cmd = np.flip(np.array(cmd,dtype=np.uint64))
            #cmd.reverse()
            #
            if simDump:
                dumpCmd = ['{:0{width}x}'.format(i, width=2) for i in cmd]
                dumpCmd.reverse()
                dumpCmd = ''.join(dumpCmd)
                dump.append(dumpCmd)
            else:
                bigCmdList.append(cmd)
                #print(cmd)
            #time.sleep(.005)
            #
            n = n + 1

        # write to text file
        if simDump:
            return dump
        else:
            split = np.concatenate(bigCmdList)
            n = 1154

 
            loopBreak = False
            count = 0
            while loopBreak == False:
                count = count+1
                print('begin: '+str(count))
                #breakpoint()
                try:
                    element = split[:n*64]
                    split = split[n*64:]
                except:
                    element = split
                    loopBreak = True
                if element.size == 0:
                    break
                #print(element)
                exitCode = dmadump.dma_dump_write(element, len(element), 1, 0, 0, 0, dmadump.DmaMethodNormal)
                if exitCode != 0:
                    breakpoint()
                #time.sleep(.4)
                print('end: '+str(count))




    def create_script(self, fname, simDump = False):
        """Generates the bash file to program HBM for the current network

        Generates the bash file needed to program the axon pointers, neuron pointers, and synapses into hbm

        Parameters
        ----------
        fname : int
            The filename to write the script to
        """
        axon_ptrs = self.create_axon_ptrs(simDump)
        neuron_ptrs = self.create_neuron_ptrs(simDump)
        synapses = self.create_synapses(simDump)

        if simDump:
            return axon_ptrs, neuron_ptrs, synapses

def main():
    with open('test' + '.pkl', 'rb') as f:
        data = pickle.load(f)

    f = fpga_compiler(data, 6271)

    f.create_script('test_config')
    #TODO: these values should not be hardcoded
    f.create_input_script(num_timesteps=0,n_inputs=1,filename='test_input')
    #print(f.create_neuron_ptrs().split('\n'))


if __name__ == '__main__':
    main()
