# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['finer']
install_requires = \
['click>=8.1.3,<9.0.0',
 'datasets==2.1.0',
 'gensim==4.2.0',
 'protobuf==3.20.3',
 'regex>=2023.6.3,<2024.0.0',
 'scikit-learn>=1.0.2',
 'seqeval==1.2.2',
 'tensorflow-addons==0.16.1',
 'tensorflow==2.8.0',
 'tf2crf==0.1.24',
 'tokenizers==0.12.1',
 'tqdm>=4.65.0,<5.0.0',
 'transformers==4.18.0',
 'wandb==0.12.16',
 'wget>=3.2,<4.0']

setup_kwargs = {
    'name': 'finer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'caiozim112',
    'author_email': 'caioopua@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
