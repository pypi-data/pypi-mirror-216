# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['delphai_fastapi', 'delphai_fastapi.companies']

package_data = \
{'': ['*']}

install_requires = \
['bson',
 'delphai-utils[config]>=3,<4',
 'fastapi-camelcase>=1.0.5,<2.0.0',
 'fastapi>=0.95,<0.96']

setup_kwargs = {
    'name': 'delphai-fastapi',
    'version': '0.1.3',
    'description': 'Package for fastAPI models',
    'long_description': 'None',
    'author': 'Berinike Tech',
    'author_email': 'berinike@delphai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
