# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hs_bridge', 'hs_bridge.FPGA_Execution', 'hs_bridge.wrapped_dmadump']

package_data = \
{'': ['*'],
 'hs_bridge.wrapped_dmadump': ['build/lib.linux-x86_64-3.10/*',
                               'build/temp.linux-x86_64-3.10/*',
                               'include/*',
                               'include/adxdma/*',
                               'include/adxdma/bc/*']}

install_requires = \
['Pebble>=5.0.3,<6.0.0',
 'PyMetis>=2020.1,<2021.0',
 'bidict>=0.22.0,<0.23.0',
 'click>=8.1.3,<9.0.0',
 'confuse>=1.7.0,<2.0.0',
 'cython>=0.29.35,<0.30.0',
 'fbpca>=1.0,<2.0',
 'k-means-constrained>=0.7.1,<0.8.0',
 'matplotlib>=3.5.2,<4.0.0',
 'metis>=0.2a5,<0.3',
 'networkx<=2.8',
 'numpy>=1.18',
 'scikit-learn>=1.2.2,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'hs-bridge',
    'version': '0.10.3',
    'description': 'Software for interacting with the CRI neuromorphic hardware',
    'long_description': None,
    'author': 'Justin Frank',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
