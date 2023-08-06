# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_sog']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.3.5,<3.0.0',
 'black>=22.1.0,<23.0.0',
 'flake8>=4.0.1,<5.0.0',
 'ipython>=8.1.1,<9.0.0',
 'isort>=5.10.1,<6.0.0']

setup_kwargs = {
    'name': 'beancount-sog',
    'version': '0.1.1',
    'description': 'Beancount Importer for Société Générale CSV files',
    'long_description': 'None',
    'author': 'Paul Khuat-Duy',
    'author_email': 'paul@khuat-duy.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Eazhi/beancount-sog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
