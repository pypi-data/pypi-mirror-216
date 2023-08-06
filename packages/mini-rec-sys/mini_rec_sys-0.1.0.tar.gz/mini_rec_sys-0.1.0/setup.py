# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mini_rec_sys',
 'mini_rec_sys.data',
 'mini_rec_sys.encoders',
 'mini_rec_sys.evaluators',
 'mini_rec_sys.sample_data',
 'mini_rec_sys.sample_data.msmarco_reranking',
 'mini_rec_sys.scorers',
 'mini_rec_sys.trainers']

package_data = \
{'': ['*']}

install_requires = \
['diskcache>=5.6.1,<6.0.0',
 'faiss-cpu>=1.7.4,<2.0.0',
 'lxml>=4.9.2,<5.0.0',
 'nltk>=3.8.1,<4.0.0',
 'numpy>=1.16.5,<1.23.0',
 'pandas>=1.0.5',
 'pydantic>=1.10.9,<2.0.0',
 'pysos>=1.3.0,<2.0.0',
 'pytorch-lightning>=2.0.4,<3.0.0',
 'torch<2.0.0',
 'transformers>=4.26.1,<5.0.0']

setup_kwargs = {
    'name': 'mini-rec-sys',
    'version': '0.1.0',
    'description': 'Toolkit to train and evaluate models for search and recommendations.',
    'long_description': '# mini-rec-sys\nTools for training and evaluating search and recommender models.\n',
    'author': 'Charles Low',
    'author_email': 'charleslow88@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
