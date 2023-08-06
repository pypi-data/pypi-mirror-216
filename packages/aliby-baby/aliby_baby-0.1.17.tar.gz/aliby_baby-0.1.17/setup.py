# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baby', 'baby.tracker', 'baby.training']

package_data = \
{'': ['*'], 'baby': ['models/*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'colorama>=0.4.4,<0.5.0',
 'configspace>=0.6.1,<0.7.0',
 'hpbandster>=0.7.4,<0.8.0',
 'imageio==2.8.0',
 'keras-tuner==1.0.1',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy==1.21.6',
 'pandas==1.3.3',
 'protobuf<=3.20.1',
 'ray>=1.13.0,<2.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.0.2',
 'scikit-plot>=0.3.7,<0.4.0',
 'tensorflow>=2.0.0,<2.9.1',
 'tqdm>=4.62.3,<5.0.0',
 'tune-sklearn>=0.4.1,<0.5.0',
 'xgboost==1.4.2']

setup_kwargs = {
    'name': 'aliby-baby',
    'version': '0.1.17',
    'description': 'Birth Annotator for Budding Yeast',
    'long_description': '# Baby\n\n## Birth Annotation for Budding Yeast\n\nNeural network code for segmenting buds from brightfield stacks.\n\n## Installation\n\nBABY requires Python 3 and [TensorFlow](https://www.tensorflow.org). For some\nversions of TensorFlow, you specifically need Python 3.6.\n\nIn any case, it is recommended that you install the package into a virtual\nenvironment (i.e., `conda create` if you are using Anaconda, or `python3 -m\nvenv` otherwise).\n\nBy default, BABY will trigger installation of the latest version of\nTensorFlow. Our experience, however, is that performance is best with\nTensorFlow version 1.14. If you want to use this version, first install that\nin your virtual environment by running:\n\n```bash\n> pip install tensorflow==1.14\n```\n\n**NB:** To make use of a GPU you should also follow the [set up\ninstructions](https://www.tensorflow.org/install/gpu#windows_setup) for\ninstalling `tensorflow-gpu`.\n\nInstall BABY by first obtaining this repository (e.g., `git clone\nhttps://git.ecdf.ed.ac.uk/jpietsch/baby.git`), and then using pip:\n\n```bash\n> pip install baby/\n```\n\nNB: If you are upgrading, then you may instead need to run: `pip install -U\nbaby/`.\n\n*Developers:* You may prefer to install an editable version:\n\n```bash\n> pip install -e baby/\n```\n\n## Run using the Python API\n\nCreate a new `BabyBrain` with one of the model sets. The `brain` contains\nall the models and parameters for segmenting and tracking cells.\n\n```python\n>>> from baby import BabyBrain, BabyCrawler, modelsets\n>>> modelset = modelsets()[\'evolve_brightfield_60x_5z\']\n>>> brain = BabyBrain(**modelset)\n```\n\nFor each time course you want to process, instantiate a new `BabyCrawler`. The\ncrawler keeps track of cells between time steps.\n\n```python\n>>> crawler = BabyCrawler(brain)\n```\n\nLoad an image time series (from the `tests` subdirectory in this example). The\nimage should have shape (x, y, z).\n\n```python\n>>> from baby.io import load_tiled_image\n>>> image_series = [load_tiled_image(\n...     \'tests/images/evolve_testG_tp{:d}_Brightfield.png\'.format(t))\n...     for t in range(1,6)]\n```\n\nSend images to the crawler in time-order (here a batch of size 1). We\nadditionally request that outlines are optimised to edge predictions, and that\nlineage assignments, binary edge-masks and volume estimates (using the conical\nmethod) should be output at each time point.\n\n```python\n>>> segmented_series = [crawler.step(\n...     img[None, ...], refine_outlines=True, assign_mothers=True,\n...     with_edgemasks=True, with_volumes=True)\n...     for img, _ in image_series]\n```\n\nFinally, save the segmentation outlines, labels, volumes and lineage assignments\nas an annotated tiled png:\n\n```python\n>>> from baby.io import save_tiled_image\n>>> for t, s in enumerate(segmented_series):\n...     save_tiled_image(255 * s[0][\'edgemasks\'].astype(\'uint8\').transpose((1, 2, 0)),\n...     \'../segout_tp{:d}.png\'.format(t + 1),\n...     {k: s[0][k] for k in (\'cell_label\', \'mother_assign\', \'volumes\')})\n```\n\n## Run via a server\n\nOnce installed, you should be able to start a server to accept segmentation\nrequests using:\n\n```bash\n> baby-phone\n```\n\nor on windows:\n\n```\n> baby-phone.exe\n```\n\nServer runs by default on [http://0.0.0.0:5101](). HTTP requests need to be\nsent to the correct URL endpoint, but the HTTP API is currently undocumented.\nThe primary client implementation is in Matlab.\n\n## Jupyter notebooks\n\nTraining scripts are saved in Jupyter notebooks in the `notebooks` folder. To\nmaintain the repository in a clean state, it\'s probably best to copy these to\nanother directory for routine use. If you want to share a notebook, you can\nthen specifically add it back to the repository at a useful checkpoint.\n\n## On how to retrain data\n\nAs of mid-2022 we aim to transition to tensorflow 2 (and then to pytorch). This means re-training all networks. We first fetch our data from skye and regenerate the train-val-test pair sets using TrainValTestPairs:\n\n```python\nfrom pathlib import Path\nfrom baby.io import TrainValTestPairs\n\ntraining_data_path = Path("/home/alan/Documents/dev/training/training-images/")\ntvt = TrainValTestPairs()\ntvt.add_from(training_data_path / "traps-prime95b-60x")\n<!-- tvt.add_from(training_data_path / "traps-evolve-60x") -->\n```\n',
    'author': 'Julian Pietsch',
    'author_email': 'jpietsch@ed.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
