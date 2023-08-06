# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autotm',
 'autotm.algorithms_for_tuning',
 'autotm.algorithms_for_tuning.bayesian_optimization',
 'autotm.algorithms_for_tuning.genetic_algorithm',
 'autotm.algorithms_for_tuning.nelder_mead_optimization',
 'autotm.fitness',
 'autotm.preprocessing',
 'autotm.visualization']

package_data = \
{'': ['*'], 'autotm': ['data_generator/*']}

install_requires = \
['PyYAML',
 'bigartm==0.9.2',
 'billiard',
 'click',
 'dataclasses-json',
 'dill',
 'gensim',
 'hyperopt',
 'mlflow',
 'nltk',
 'numpy',
 'pandas',
 'plotly',
 'pydantic',
 'pymongo',
 'pymystem3',
 'pytest',
 'scikit-learn',
 'scipy',
 'spacy',
 'spacy-langdetect',
 'tqdm']

setup_kwargs = {
    'name': 'autotm',
    'version': '0.1.0',
    'description': 'Automatic hyperparameters tuning for topic models (ARTM approach) using evolutionary algorithms',
    'long_description': '# AutoTM\n\n[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)\n![build](https://github.com/ngc436/AutoTM/actions/workflows/build.yaml/badge.svg)\n[![GitHub Repo stars](https://img.shields.io/github/stars/ngc436/AutoTM?style=social)](https://github.com/ngc436/AutoTM/stargazers)\n\nAutomatic parameters selection for topic models (ARTM approach) using evolutionary algorithms. \nAutoTM provides necessary tools to preprocess english and russian text datasets and tune topic models.\n\n## What is AutoTM?\nTopic modeling is one of the basic methods for EDA of unlabelled text data. While ARTM (additive regularization \nfor topic models) approach provides the significant flexibility and quality comparative or better that neural \napproaches it is hard to tune such models due to amount of hyperparameters and their combinations.\n\nTo overcome the tuning problems AutoTM presents an easy way to represent a learning strategy to train specific models for input corporas.\n\n<img src="docs/img/strategy.png" alt="Learning strategy representation" height=""/>\n\nOptimization procedure is done by genetic algorithm which operators are specifically tuned for \nthe task. To speed up the procedure we also implemented surrogate modeling that, for some iterations, \napproximate fitness function to reduce computation costs on training topic models.\n\n<img src="docs/img/img_library_eng.png" alt="Library scheme" height=""/>\n\n\n## Installation\n\n! Note: The functionality of topic models training is available only for linux distributions.\n\n```pip install -r requirements.txt```  \n\n```python -m spacy download en_core_web_sm```\n\n```export PYTHONPATH="${PYTHONPATH}:/path/to/src"```\n\n[//]: # (## Dataset and )\n\n## Quickstart\n\nThe notebook with an example is available in ```examples``` folder.\n\n## Distributed version\n\nDistributed version to run experiments on kubernetes is available in ```autotm-distributed``` brunch. Still this version is in development stage and will be transfered to separate repository.\n\n## Backlog:\n- [ ] Add tests\n- [ ] Add new multi-stage \n \n## Citation\n\n```bibtex\n@article{10.1093/jigpal/jzac019,\n    author = {Khodorchenko, Maria and Butakov, Nikolay and Sokhin, Timur and Teryoshkin, Sergey},\n    title = "{ Surrogate-based optimization of learning strategies for additively regularized topic models}",\n    journal = {Logic Journal of the IGPL},\n    year = {2022},\n    month = {02},\n    issn = {1367-0751},\n    doi = {10.1093/jigpal/jzac019},\n    url = {https://doi.org/10.1093/jigpal/jzac019},}\n\n```\n',
    'author': 'Khodorchenko Maria',
    'author_email': 'mariyaxod@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://autotm.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
