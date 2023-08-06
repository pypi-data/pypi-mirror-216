# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['eiffel']

package_data = \
{'': ['*']}

extras_require = \
{'darwin:sys_platform == "darwin"': ['tensorflow-metal>=0.6.0,<0.7.0',
                                     'tensorflow-macos>=2.10.0,<2.11.0',
                                     'grpcio>=1.37.0,<2.0',
                                     'h5py>=3.6.0,<3.7',
                                     'numpy>=1.23.2,<1.23.3',
                                     'protobuf>=3.19.1,<3.20']}

setup_kwargs = {
    'name': 'eiffel-framework',
    'version': '0.1.3',
    'description': 'Evaluation Framework for FL-based intrusion detection using Flower.',
    'long_description': '# eiffel\nEvaluation framework for FL-based intrusion detection using Flower.\n',
    'author': 'phdcybersec',
    'author_email': '82591009+phdcybersec@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
