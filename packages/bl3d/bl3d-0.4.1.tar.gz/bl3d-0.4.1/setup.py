# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bl3d']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bl3d',
    'version': '0.4.1',
    'description': 'Domain Driven Design library',
    'long_description': "# bl3d – A Domain Driven Design library\n\nBioneland's Domain Driven Design library (bl3d, pronounced */'bled/*) is a collection\nof classes to write domain driven designed software.\n",
    'author': 'Tanguy Le Carrour',
    'author_email': 'tanguy@bioneland.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.easter-eggs.org/bioneland/bl3d',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
