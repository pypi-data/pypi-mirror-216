# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['client', 'client.api', 'client.batch', 'client.cli', 'client.parser']

package_data = \
{'': ['*']}

install_requires = \
['geneweaver-core>=0.1.0a1,<0.2.0',
 'openpyxl>=3.1.2,<4.0.0',
 'pydantic[dotenv]>=1.10.7,<2.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest>=7.2.2,<8.0.0',
 'requests>=2.28.2,<3.0.0',
 'rich>=13.4.2,<14.0.0',
 'typer[all]>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['gweave = geneweaver.client.cli.main:cli',
                     'gweaver = geneweaver.client.cli.main:cli']}

setup_kwargs = {
    'name': 'geneweaver-client',
    'version': '0.0.1a0.dev1',
    'description': 'A Python Client for the Geneweaver API',
    'long_description': '# Geneweaver Client\n\nThis is a client for the [Geneweaver](https://geneweaver.org) API. It is written in \nPython 3.9 and is intended to be used as a library for other applications. It can also \nbe used as a command line tool.\n\n## Installation\n\n### From PyPI\n\n```bash\npip install geneweaver-client\n```\n\n### From Source\nInstalling from source requires python 3.9 and [poetry](https://python-poetry.org/).\n\n\n```bash\ngit clone $GIT_URL\ncd geneweaver-client\npoetry install\n```\n\n## Usage\n\n### As a library\n\nComing soon.\n\n### As a command line tool\n\n```bash\ngweave --help\n```',
    'author': 'Jax Computational Sciences',
    'author_email': 'cssc@jax.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bergsalex.github.io/geneweaver-docs/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
