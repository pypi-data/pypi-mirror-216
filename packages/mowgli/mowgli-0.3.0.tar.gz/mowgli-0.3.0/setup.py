# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mowgli']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.8.0,<0.9.0',
 'matplotlib>=3.0.0,<4.0.0',
 'mudata>=0.2.1,<0.3.0',
 'numpy>=1.0.0,<2.0.0',
 'scanpy>=1.0.0,<2.0.0',
 'scikit-learn>=1.0.0,<2.0.0',
 'scipy>=1.0.0,<2.0.0',
 'torch>=1.0.0,<2.0.0',
 'tqdm>=4.0.0,<5.0.0']

extras_require = \
{'dev': ['pre-commit>=3.1.1,<4.0.0'],
 'docs': ['nbsphinx>=0.8.12,<0.9.0', 'furo>=2022.12.7,<2023.0.0'],
 'full': ['gprofiler-official>=1.0.0,<2.0.0', 'leidenalg>=0.9.1,<0.10.0']}

setup_kwargs = {
    'name': 'mowgli',
    'version': '0.3.0',
    'description': 'Mowgli is a novel method for the integration of paired multi-omics data with any type and number of omics, combining integrative Nonnegative Matrix Factorization and Optimal Transport.',
    'long_description': '# Mowgli: Multi Omics Wasserstein inteGrative anaLysIs\n[![Tests](https://github.com/gjhuizing/Mowgli/actions/workflows/main.yml/badge.svg)](https://github.com/gjhuizing/Mowgli/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/cantinilab/Mowgli/branch/main/graph/badge.svg?token=UBUJF7098Q)](https://codecov.io/gh/cantinilab/Mowgli)\n[![Documentation Status](https://readthedocs.org/projects/mowgli/badge/?version=latest)](https://mowgli.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://img.shields.io/pypi/v/mowgli?color=blue)](https://img.shields.io/pypi/v/mowgli?color=blue)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nMowgli is a novel method for the integration of paired multi-omics data with any type and number of omics, combining integrative Nonnegative Matrix Factorization and Optimal Transport. [Read the preprint!](https://www.biorxiv.org/content/10.1101/2023.02.02.526825v2)\n\n![figure](figure.png)\n\n## Install the package\n\nMowgli is implemented as a Python package seamlessly integrated within the scverse ecosystem, in particular Muon and Scanpy.\n\n### via PyPI (recommended)\n\nOn all operating systems, the easiest way to install Mowgli is via PyPI. Installation should typically take a minute and is continuously tested with Python 3.8 on an Ubuntu virtual machine.\n\n```bash\npip install mowgli\n```\n\n### via GitHub (development version)\n\n```bash\ngit clone git@github.com:cantinilab/Mowgli.git\npip install ./Mowgli/\n```\n\n## Getting started\n\nMowgli takes as an input a Muon object and populates its `obsm` and `uns` fiels with the embeddings and dictionaries, respectively. Visit [mowgli.rtfd.io](https://mowgli.rtfd.io/) for more documentation and tutorials.\n\nYou may download a preprocessed 10X Multiome demo dataset [here](https://figshare.com/s/4c8e72cbb188d8e1cce8).\n\nA GPU is not required for small datasets, but is strongly recommmended above 1,000 cells. On CPU, the [cell lines demo](https://mowgli.readthedocs.io/en/latest/vignettes/Liu%20cell%20lines.html) (206 cells) should run in under 5 minutes and the [PBMC demo](https://mowgli.readthedocs.io/en/latest/vignettes/PBMC.html) (500 cells) should run in under 10 minutes (tested on a Ubuntu 20.04 machine with an 11th gen i7 processor).\n\n```python\nimport mowgli\nimport mudata as md\nimport scanpy as sc\n\n# Load data into a Muon object.\nmdata = md.read_h5mu("my_data.h5mu")\n\n# Initialize and train the model.\nmodel = mowgli.models.MowgliModel(latent_dim=15)\nmodel.train(mdata)\n\n# Visualize the embedding with UMAP.\nsc.pp.neighbors(mdata, use_rep="W_OT")\nsc.tl.umap(mdata)\nsc.pl.umap(mdata)\n```\n\n## Our preprint\n\n```bibtex\n@article{huizing2023paired,\n  title={Paired single-cell multi-omics data integration with Mowgli},\n  author={Huizing, Geert-Jan and Deutschmann, Ina Maria and Peyre, Gabriel and Cantini, Laura},\n  journal={bioRxiv},\n  pages={2023--02},\n  year={2023},\n  publisher={Cold Spring Harbor Laboratory}\n}\n```\n\nIf you\'re looking for the repository with code to reproduce the experiments in our preprint, [here is is!](https://github.com/cantinilab/mowgli_reproducibility)\n',
    'author': 'Geert-Jan Huizing',
    'author_email': 'huizing@ens.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
