# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aequilibrium', 'aequilibrium.utils']

package_data = \
{'': ['*']}

install_requires = \
['imbalanced-learn<0.9',
 'matplotlib<3.6',
 'numpy>=1.21,<2.0',
 'pandas>=1.3,<2.0',
 'scikit-learn<1.1',
 'seaborn<0.12']

setup_kwargs = {
    'name': 'aequilibrium',
    'version': '1.0.1',
    'description': 'Python package for classification of imbalanced data.',
    'long_description': None,
    'author': 'Luke Beasley',
    'author_email': 'beasleyl2@aetna.com',
    'maintainer': 'Luke Beasley',
    'maintainer_email': 'beasleyl2@aetna.com',
    'url': 'https://github.com/cvs-health/aequilibrium',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.8',
}


setup(**setup_kwargs)
