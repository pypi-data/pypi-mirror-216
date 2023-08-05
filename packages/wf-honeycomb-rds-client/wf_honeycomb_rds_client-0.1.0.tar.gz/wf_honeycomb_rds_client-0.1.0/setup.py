# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['honeycomb_rds_client']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5,<2.0',
 'toml>=0.10.2,<0.11.0',
 'wf-honeycomb-io>=2.1,<3.0',
 'wf-postgres-client>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'wf-honeycomb-rds-client',
    'version': '0.1.0',
    'description': 'A client for communicating with the RDS database underlying Honeycomb',
    'long_description': '# honeycomb_rds_client\n\nA client for communicating with the RDS database underlying Honeycomb\n\n## Installation\n\n`pip install wf-honeycomb-rds-client`\n\n## Development\n\n### Requirements\n\n* [Poetry](https://python-poetry.org/)\n* [just](https://github.com/casey/just)\n\n### Install\n\n`poetry install`\n\n\n#### Install w/ Python Version from PyEnv\n\n```\n# Specify pyenv python version\npyenv shell --unset\npyenv local <<VERSION>>\n\n# Set poetry python to pyenv version\npoetry env use $(pyenv which python)\npoetry cache clear . --all\npoetry install\n```\n\n## Task list\n* TBD\n',
    'author': 'Theodore Quinn',
    'author_email': 'ted.quinn@wildflowerschools.org',
    'maintainer': 'Theodore Quinn',
    'maintainer_email': 'ted.quinn@wildflowerschools.org',
    'url': 'https://github.com/WildflowerSchools/wf-honeycomb-rds-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
