# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['errmod']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'errmod',
    'version': '0.1.1',
    'description': 'String stuff',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
