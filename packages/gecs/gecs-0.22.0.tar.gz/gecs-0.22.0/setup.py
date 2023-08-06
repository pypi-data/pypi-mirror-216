# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gecs', 'gecs.utils']

package_data = \
{'': ['*']}

install_requires = \
['lightgbm==3.3.5',
 'matplotlib==3.7.1',
 'numpy==1.23.5',
 'pandas==1.5.2',
 'poetry==1.3.2',
 'pytest==7.2.1',
 'scikit-learn==1.2.2',
 'scipy==1.10.1',
 'tqdm==4.65.0',
 'typer==0.9.0']

setup_kwargs = {
    'name': 'gecs',
    'version': '0.22.0',
    'description': 'LightGBM Classifier with integrated bayesian hyperparameter optimization',
    'long_description': '',
    'author': 'Leon Luithlen',
    'author_email': 'leontimnaluithlen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/0xideas/sequifier',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
