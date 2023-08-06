# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hs_api']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'bidict>=0.22.0,<0.23.0',
 'connectome-utils>=0.1.0,<0.2.0',
 'fxpmath>=0.4.8,<0.5.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numba>=0.55.1,<0.56.0',
 'numpy>=1.18',
 'torch>=2.0.1,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'hs-api',
    'version': '0.1.3',
    'description': 'CRI User Software',
    'long_description': None,
    'author': 'Justin Frank & Abhinav Uppal',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
