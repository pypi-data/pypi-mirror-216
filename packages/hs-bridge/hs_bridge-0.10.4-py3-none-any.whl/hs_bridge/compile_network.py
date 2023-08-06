import numpy as np
from tqdm import tqdm
from hs_bridge.config import *
import sys
from ast import literal_eval
from math import ceil
from bidict import bidict
import logging

#attempt to import the partitioning code, if it is unavailable fall back to single core only opperation
try:
    from cri_simulations.partitioning_code.hierarchical_partition import partition as netPart
    partLoad = True
except:
    partLoad = False
    logging.warning("partitioning library failed to load, multicore disabled")

################################################################
# Note: ARCH, N_NG, PTRS_PER_ROW, and DATA_PER_ROW are read in #
# from a YAML config. These values are specific to the current #
# itteration of the CRI hardware and should NOT be altered     #
# unless the corresponding parameters in the hardware change   #
################################################################

sixteen_flag = True #This currently exists for legacy reasons, to work properly with post spring 2022 bitstreams it must be set to true



def generate_local_neurons(axons, connections, axonAssignments, neuronAssignments, n_cores):
    """Clusters axons and neurons into seperate dictionaries by the core they are assigned to.
       
       This function takes a dictionary of axon objects, a dictionary of neuron objects and a set of
       core assignments for the axons and neurons and constructs a dicitonary containing a core
       specific axon and neuron dictionary for each core containing only the axons/neurons assigned to that core.

    Parameters
    ----------
    axons : dict
        Dictionary specifying axons in the network. Key: Axon Number: Synapse Weights
    network : dict
        Dictionary specifying neurons in the network. Key: Neuron Number Value: Synapse Weights
    axonAssignments : dict
        Dictionary specifying axons mapped to each core. Key: axon key Value: assigned core number
    neuronAssignments : dict
        Dictionary specifying neurons mapped to each core. Key: neuron key Value: assigned core number
    n_cores : int
        The number of cores peresent in the CRI system

    Returns
    -------
    masterDict : dict
        Dictionary containing the core specific axon and neuron dictionaries for each core. 
    """
    masterDict = {}
    for i in range(n_cores):
        masterDict[i] = {}
        masterDict[i]["axons"] = {}
        masterDict[i]["connections"] = {}
    for axonKey in axons.keys():
        core = axonAssignments[axonKey] #problem, how do we handle axon indicies across cores?
        masterDict[core]["axons"][axonKey] = axons[axonKey]
    for neuronKey in connections.keys():
        core = neuronAssignments[neuronKey] #problem, how do we handle axon indicies across cores?
        masterDict[core]["connections"][neuronKey] = connections[neuronKey]
    return masterDict
        


def get_cores():
    """Get's the number of cores to map the network to
    Returns
    -------
    n_cores : int
        The number of cores to map the network to
    """
    # Get the number of cores to map to
    n_cores = 0
    for fpga_cluster_num, fpga_cluster in enumerate(ARCH):
        for fpga_num, fpga in enumerate(fpga_cluster["FPGA"]):
            for core_cluster_num, core_cluster, in enumerate(fpga["Core_cluster"]):
                for core_num in range(int(core_cluster["Cores"])):
                    n_cores += 1
    return n_cores


def load_network(input, connex, output):
    """Loads the network specification.

    This function loads the inputs and connections specified for the network.
    Also determines the number of FPGA cores to be used.
    THIS HAS BEEN DEPRECATED

    Parameters
    ----------
    input : str, optional
        Path to file specifying network inputs. (the default is the path in config.yaml)
    connex : str, optional
        Path to file specifying network connections. (the default is the path in config.yaml)

    Returns
    -------
    axons : dict
        Dictionary specifying axons in the network. Key: axon number Value: Synapse Weights
    connections : dict
        Dictionary specifying neurons in the network. Key: Neuron Number Value: Synapse Weights
    inputs : dict
        Dictionary specifying inputs to the network. Key, Time Step Value, axon
    outputs : dict
        TODO: I'm not sure what the outputs are for. I belive it's unused
    ncores : int
        The number of cores peresent in the CRI system

    """
    axons = {}
    connections = {}
    inputs = {}
    outputs = {}

    # Load in the connectivity file
    ax = None
    with open(connex, "r") as f:
        for line in f:
            if not line.startswith("#"):
                if "axons" in line.lower():
                    ax = True
                elif "neurons" in line.lower():
                    ax = False
                else:
                    pre, post = line.split(":")
                    weights = literal_eval(post.strip())
                    weights = [(int(i[0]), float(i[1])) for i in weights]
                    if ax:
                        axons[int(pre.strip())] = weights
                    else:
                        connections[int(pre.strip())] = weights

    # Load in the inputs file
    with open(input, "r") as f:
        for line in f:
            if not line.startswith("#"):
                pre, post = line.split(":")
                inputs[int(pre.strip())] = literal_eval(post.strip())

    with open(output, "r") as f:
        for line in f:
            if not line.startswith("#"):
                pre, post = line.split(":")
                outputs[int(pre.strip())] = literal_eval(post.strip())

    # Get the number of cores to map to
    # n_cores = 0
    # for fpga_cluster_num, fpga_cluster in enumerate(ARCH):
    #    for fpga_num, fpga in enumerate(fpga_cluster['FPGA']):
    #        for core_cluster_num, core_cluster, in enumerate(fpga['Core_cluster']):
    #            for core_num in range(int(core_cluster['Cores'])):
    #                n_cores += 1
    n_cores = get_cores()

    #print(n_cores)

    # assignment = partition(connex,n_cores)

    assert len(connections.keys()) - 1 in connections.keys()

    return axons, connections, inputs, outputs, n_cores




def partition(connectome, n_cores):
    """Creates adjacency list

    Uses the partitioning algorithm to partition the neurons in the network and applies core assignments to neurons and axons in the connectome object

    Parameters
    ----------
    network : connectome object
        An object contatining the network topology information
    ncores : int
        The number of cores peresent in the CRI system

    Notes
    -----
    This function calls the apply_partition method of the connectome object, which mutates 'connectome'

    """
    networkConnectivity = connectome.get_part_format()

    #TODO: get rid of this, it's just for some quick and dirty debugging
    #n_cores =2
    # No partitioning
    if n_cores == 1:
        membership = {k: 0 for k in range(len(networkConnectivity))}
        #return {k: 0 for k, v in connectome.connectomeDict.items()}
         #return {k: 0 for k, v in axons.items()},{k: 0 for k, v in connections.items()}

    # Partition the network
    else:
        if (partLoad):
            membership = netPart(data = networkConnectivity,n_clusters = n_cores) #n_clusters is just the number of cores to partition the network across
        else:
            logging.error("partitioning library failed to load, multicore partitioning skipped")

    connectome.apply_partition(membership)
    #breakpoint()


def map_to_hbm_fpga(connectome, n_cores, to_fpga=True):
    """Creates HBM Data Structure

    Creates a representation of the axon pointers, neuron pointers, and synapse weights in HBM memory

    Parameters
    ----------
    axons : dict
        Dictionary specifying axons in the network. Key: Axon Number Value: Synapse Weights
    network : dict
        Dictionary specifying neurons in the network. Key: Neuron Number Value: Synapse Weights
    assignment : dict
        Dictionary specifying neurons mapped to each core. Key: core number Value: tuple of (neuron number, core number)
    n_cores : int
        The number of cores peresent in the CRI system
    to_fpga : bool, optional
        This parameter is depracated and has no effect. (the default is True)

    Returns
    -------
    hbm : dict
        Dictionary specifying the structure of data in memory for each core. Key: core number Value: tuple of (pointer,data) where pointer is a numpy array of tuples representing offsets into hbm memory and data is a list of lists tuples representing synapses.
    """

    # Should operate indpendent of the number of clusters
    # Return a dict of hbm ptrs and data for each cluster

    hbm = {}

    rows_per_ptr = ceil(N_NG / DATA_PER_ROW) #the number of rows needed to represent one 'slot' in hbm for all neuron groups

    for core_idx in range(n_cores):
        current = 0 #the current index into HBM measured in number of rows
        axon_ptrs = []
        axon_data = []

        ############################
        # Handle the Axons
        ############################
        axons = connectome.get_axons()
        for axonKey in tqdm(axons): #iterate through all axons
            axon = axons[axonKey]
            weights = axon.get_synapses() # synapses of the axon
            used_weights = np.ones(len(weights))
            num_rows = 0
            row_offset = 0 
             
            if not weights: #the axon has no synapses
                logging.warning("Axon with no synapses detected") #It would be very unusual to intentionally instantiate an axon with no synapses
                if sixteen_flag:
                    # if there is no weights we append NG_Num number of rows of empty synapses and a pointer to those rows
                    for i in range(rows_per_ptr):#append the minimum number of rows
                        axon_data.append([(0, 0, 0) for r in range(DATA_PER_ROW)])
                    axon_ptrs.append((current, current + (rows_per_ptr - 1)))
                    current += rows_per_ptr
                    row_offset += 1
                else:
                    axon_data.append([(0, 0, 0) for r in range(DATA_PER_ROW)])
                    axon_ptrs.append((current, current))
                    current += 1
                    row_offset += 1
                continue

            while sum(used_weights) != 0:
                row = np.zeros(N_NG).astype(object)
                for w in range(len(weights)):
                    if used_weights[w] != 0:
                        column = weights[w].get_postsynapticNeuron().get_coreTypeIdx() % N_NG
                        if row[column] == 0:
                            row[column] = (
                                0,
                                np.floor(weights[w].get_postsynapticNeuron().get_coreTypeIdx() / N_NG),
                                weights[w].get_weight(),
                            )
                            weights[w].set_index(row_offset, column)

                            used_weights[w] = 0


                row = [r if r != 0 else (0, 0, 0) for r in row]
                if sixteen_flag:
                    num_rows += rows_per_ptr
                    temp = np.empty(len(row), dtype=object)
                    temp[:] = row
                    axon_row_list = temp.reshape(-1, DATA_PER_ROW)
                    axon_row_list = np.flip(axon_row_list, axis=0)
                    for axon_row in axon_row_list:
                        axon_data.append(axon_row.tolist())
                    row_offset += 1
                else:
                    num_rows += 1  # For the pointers
                    axon_data.append(row)
                    row_offset += 1

            if sixteen_flag:
                axon_ptrs.append((current, current + num_rows - 1))
                current += num_rows
            else:
                axon_ptrs.append((current, current + num_rows - 1))
                current += num_rows

        if sixteen_flag:
            if len(axon_ptrs) % N_NG != 0:
                # make sure the row is filled with axon pointers TODO: do we just care the row is full or should the number
                # of axon pointers be divisable by 16
                # The correct answer is the total number of axon pointers should be evenly divisable by N_NG
                for j in range(N_NG - len(axon_ptrs) % N_NG):
                    axon_ptrs.append((current, current + rows_per_ptr - 1))
                    current += rows_per_ptr
                    row_offset += 1
                    for i in range(rows_per_ptr):
                        axon_data.append([(0, 0, 0) for r in range(DATA_PER_ROW)])
        else:
            if len(axon_ptrs) % DATA_PER_ROW != 0:
                for j in range(DATA_PER_ROW - len(axon_ptrs) % DATA_PER_ROW):
                    axon_ptrs.append((current, current))
                    current += 1
                    row_offset += 1
                    axon_data.append([(0, 0, 0) for r in range(DATA_PER_ROW)])

        dt = np.dtype("object,object")
        if sixteen_flag:
            axon_ptrs = np.array(axon_ptrs, dtype=dt).reshape((-1, DATA_PER_ROW))
        else:
            axon_ptrs = np.array(axon_ptrs, dtype=dt).reshape((-1, DATA_PER_ROW))

        #################################
        # Handle the Neurons
        #################################
        ptrs = []
        data = []
        neurons = connectome.get_neurons()
        
        for neuronKey in tqdm(neurons):
            neuron = neurons[neuronKey]
            weights = neuron.get_synapses()
            used_weights = np.ones(len(weights))
            num_rows = 0
            row_offset = 0 

            if not weights:
                if sixteen_flag:
                    # if no weights create a pointer to NG_num rows of zero synapses
                    for i in range(rows_per_ptr):
                        data.append([(0, 0, 0) for r in range(DATA_PER_ROW)])
                    # data.append([(0,0,0) for r in range(DATA_PER_ROW)])
                    ptrs.append((current, current + (rows_per_ptr - 1)))
                    current += rows_per_ptr
                    row_offset += 1
                else:
                    data.append([(0, 0, 0) for r in range(DATA_PER_ROW)])
                    ptrs.append((current, current))
                    current += 1
                    row_offset += 1
                continue

            space_for_spike = False
            while sum(used_weights) != 0:
                # Create a row
                row = np.zeros(N_NG).astype(object)

                for w in range(len(weights)):
                    if used_weights[w] != 0:
                        column = weights[w].get_postsynapticNeuron().get_coreTypeIdx() % N_NG
                        if row[column] == 0:
                            row[column] = (
                                0,
                                np.floor(weights[w].get_postsynapticNeuron().get_coreTypeIdx() / N_NG),
                                weights[w].get_weight(),
                            )
                            weights[w].set_index(row_offset, column)
                            used_weights[w] = 0

                row = [r if r != 0 else (0, 0, 0) for r in row]
                if sixteen_flag:
                    num_rows += rows_per_ptr
                    row_offset += 1
                else:
                    num_rows += 1  # For the pointers
                    row_offset += 1
                if (0, 0, 0) in row:
                    space_for_spike = True

                if not row:
                    logging.info("empty neuron row found")
                if sixteen_flag:
                    # num_rows += rows_per_ptr
                    temp = np.empty(
                        len(row), dtype=object
                    )  # numpy get's weird about reshaping object arrays
                    temp[:] = row
                    # print(temp)
                    neuron_row_list = temp.reshape(-1, DATA_PER_ROW)
                    neuron_row_list = np.flip(neuron_row_list, axis=0)
                    # print(axon_row_list)
                    # print(DATA_PER_ROW)
                    for neuron_row in neuron_row_list:
                        # print(axon_row.tolist())
                        data.append(neuron_row.tolist())
                else:
                    data.append(row)

            # No place for spike data, we add an additional empty row
            # TODO: is it sufficient to simply add one extra row or does in
            # need to be rows_per_ptr number of empty rows?
            # I'm pretty sure it needs to be rows_per_ptr number of empty rows
            if not space_for_spike:
                if sixteen_flag:
                    for i in range(rows_per_ptr):
                        data.append([(0, 0, 0) for r in range(DATA_PER_ROW)])
                    # data.append([(0,0,0) for r in range(DATA_PER_ROW)])
                    num_rows += rows_per_ptr
                    row_offset += 1
                else:
                    data.append([(0, 0, 0) for r in range(DATA_PER_ROW)])
                    num_rows += 1
                    row_offset += 1

            ptrs.append((current, current + num_rows - 1))
            current += num_rows

        if len(ptrs) % N_NG != 0:
            #print("need to pad neuron pointers")
            #print(ptrs)
            if sixteen_flag:
                for j in range(N_NG - len(ptrs) % N_NG):
                    ptrs.append((current, current + (rows_per_ptr - 1)))
                    current += rows_per_ptr
                    row_offset += 1
                    for i in range(rows_per_ptr):
                        data.append([(0, 0, 0) for r in range(DATA_PER_ROW)])
            else:
                for j in range(DATA_PER_ROW - len(ptrs) % DATA_PER_ROW):
                    ptrs.append((current, current))
                    current += 1
                    row_offset += 1
                    data.append([(0, 0, 0) for r in range(DATA_PER_ROW)])

        dt = np.dtype("object,object")
        if sixteen_flag:
            ptrs = np.array(ptrs, dtype=dt).reshape((-1, DATA_PER_ROW))
        else:
            ptrs = np.array(ptrs, dtype=dt).reshape((-1, DATA_PER_ROW))

        data = axon_data + data



        hbm[core_idx] = (axon_ptrs, ptrs, data)
        
        ptrs = np.vstack((axon_ptrs, ptrs))
        

       

    return hbm # TODO this will need to be fixed for when we move to multicore, it currently only returns hbm for a single core


def compileNetwork(
    loadFile=False, connectome=None, inputs=None, outputs=None):
    """Creates simulation and FPGA data structures

    Creates a representation of the axon pointers, neuron pointers, and synapse weights in HBM memory both in the format used to produce the commands to program the actual FPGA and in the format expected by the hardware simulator.

    Parameters
    ----------
    loadFile : bool
        if True network topology is read from files on disk. This option is deprecated
    connectome : obj
        object encapsulating axons and connections
    inputs : dict
        Dictionary specifying inputs to the network. Key: Time Step Value: List of active axons 
    outputs : dict
        TODO: I'm not sure what the outputs are for. I belive it's unused
    Returns
    -------
    fpga : dict
        Dictionary specifying the hbm structure for each core expected by the hardware simulator. Key: core number Value: tuple of (pointer,data) where pointer is a numpy array and data is a list of lists of tuples.
    axonLength : int
        number of axons specified in the network

"""
    if loadFile:
        axons, network, input, output, n_cores = load_network()
    else:
        if connectome == None or outputs == None:
            raise ValueError(
                "compileNetwork was called with loadFile set to False and one or more input dicitonary was empty"
            )
        # normally load_network returns n_cores, instead we'll just do it explicetly

        n_cores = get_cores()

    partition(connectome, n_cores)
    #generate_local_neurons(axons,connections,axonAssignments , neuornAssignments, n_cores)
    #you're going to have to generate an hbm mapping for every core
    fpga = map_to_hbm_fpga(connectome, n_cores)
    axonLength = len(connectome.get_axons())
    if loadFile:
        return outputs, fpga, axonLength
    else:
        return fpga, axonLength


def main():
    compileNetwork()


if __name__ == "__main__":
    main()
