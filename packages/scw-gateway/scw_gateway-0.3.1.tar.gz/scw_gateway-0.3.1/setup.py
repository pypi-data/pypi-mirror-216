# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli', 'cli.infra']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'loguru==0.6.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'scaleway>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['scwgw = cli.cli:cli']}

setup_kwargs = {
    'name': 'scw-gateway',
    'version': '0.3.1',
    'description': 'CLI to deploy and manage a self-hosted Kong gateway on Scaleway Serverless Ecosystem',
    'long_description': '',
    'author': 'Simon Shillaker',
    'author_email': 'sshillaker@scaleway.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
