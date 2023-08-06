# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wineml']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wineml',
    'version': '0.0.1',
    'description': 'Python library for WineML Registry',
    'long_description': '',
    'author': 'Melvin Low',
    'author_email': 'lowbingjiun@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
