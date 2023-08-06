# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owe_python_sdk',
 'owe_python_sdk.client',
 'owe_python_sdk.events',
 'owe_python_sdk.middleware',
 'owe_python_sdk.runtime']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.9,<2.0.0']

setup_kwargs = {
    'name': 'owe-python-sdk',
    'version': '0.0.1a2',
    'description': '',
    'long_description': None,
    'author': 'Nathan Freeman',
    'author_email': 'nfreeman@tacc.utexas.edu.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tapis-project/tapis-workflows',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
