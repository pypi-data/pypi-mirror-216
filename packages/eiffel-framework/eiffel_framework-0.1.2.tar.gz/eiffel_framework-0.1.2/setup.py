# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['eiffel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eiffel-framework',
    'version': '0.1.2',
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
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
