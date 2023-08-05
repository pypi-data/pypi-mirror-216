# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starbear']

package_data = \
{'': ['*']}

install_requires = \
['hrepr>=0.5.0,<0.6.0',
 'starlette>=0.20.3,<0.21.0',
 'uvicorn>=0.17.6,<0.18.0',
 'websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'starbear',
    'version': '0.0.4',
    'description': 'Framework for easy small local web apps or programs',
    'long_description': 'None',
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
