# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioredisorm']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=2.0.1,<3.0.0', 'asyncio>=3.4.3,<4.0.0']

setup_kwargs = {
    'name': 'aioredisorm',
    'version': '0.1.0',
    'description': 'A Python class for interacting with Redis using asyncio and aioredis.',
    'long_description': None,
    'author': 'fadedreams7',
    'author_email': 'fadedreams7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
