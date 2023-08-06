# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['barnacle', 'barnacle.tests']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0',
 'numpy>=1.23,<2.0',
 'opt-einsum>=3.3.0,<4.0.0',
 'plotly>=5.13.1,<6.0.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'scipy>=1.9.0,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'tensorly-viz>=0.1.7,<0.2.0',
 'tensorly>=0.8.0,<0.9.0',
 'threadpoolctl>=3.1.0,<4.0.0']

setup_kwargs = {
    'name': 'barnacle',
    'version': '0.1.0',
    'description': 'unsupervised clustering analysis via sparse tensor decomposition',
    'long_description': '# barnacle\n\n',
    'author': 'Stephen Blaskowski',
    'author_email': 'stephen.blaskowski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/blasks/barnacle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
