# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umapi_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'schema>=0.7.5,<0.8.0',
 'umapi-client>=3.0,<4.0']

entry_points = \
{'console_scripts': ['umapi = umapi_cli.cli:app']}

setup_kwargs = {
    'name': 'umapi-cli',
    'version': '2.0.0a1',
    'description': 'User Management API CLI Tool',
    'long_description': 'None',
    'author': 'Andrew Dorton',
    'author_email': 'adorton@adobe.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
