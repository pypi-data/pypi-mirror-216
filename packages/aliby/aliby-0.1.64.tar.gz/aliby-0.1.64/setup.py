# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'agora': 'src/agora',
 'agora.io': 'src/agora/io',
 'agora.utils': 'src/agora/utils',
 'extraction': 'src/extraction',
 'extraction.core': 'src/extraction/core',
 'extraction.core.functions': 'src/extraction/core/functions',
 'extraction.core.functions.custom': 'src/extraction/core/functions/custom',
 'logfile_parser': 'src/logfile_parser',
 'postprocessor': 'src/postprocessor',
 'postprocessor.core': 'src/postprocessor/core',
 'postprocessor.core.functions': 'src/postprocessor/core/functions',
 'postprocessor.core.multisignal': 'src/postprocessor/core/multisignal',
 'postprocessor.core.processes': 'src/postprocessor/core/processes',
 'postprocessor.core.reshapers': 'src/postprocessor/core/reshapers',
 'postprocessor.routines': 'src/postprocessor/routines'}

packages = \
['agora',
 'agora.io',
 'agora.utils',
 'aliby',
 'aliby.bin',
 'aliby.io',
 'aliby.lineage',
 'aliby.tile',
 'aliby.track',
 'aliby.utils',
 'extraction',
 'extraction.core',
 'extraction.core.functions',
 'extraction.core.functions.custom',
 'logfile_parser',
 'postprocessor',
 'postprocessor.core',
 'postprocessor.core.functions',
 'postprocessor.core.multisignal',
 'postprocessor.core.processes',
 'postprocessor.core.reshapers',
 'postprocessor.routines']

package_data = \
{'': ['*'],
 'aliby.bin': ['2023_03_20_annotation/*'],
 'logfile_parser': ['grammars/*']}

install_requires = \
['Bottleneck>=1.3.5,<2.0.0',
 'GitPython>=3.1.27,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'dask>=2021.12.0,<2022.0.0',
 'flatten-dict>=0.4.2,<0.5.0',
 'gaussianprocessderivatives>=0.1.5,<0.2.0',
 'h5py==2.10',
 'imageio==2.8.0',
 'numpy>=1.21.6',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'p-tqdm>=1.3.3,<2.0.0',
 'pandas>=1.3.3',
 'pathos>=0.2.8,<0.3.0',
 'py-find-1st>=1.1.5,<2.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'scikit-image>=0.18.1',
 'scikit-learn>=1.0.2',
 'scipy>=1.7.3',
 'tqdm>=4.62.3,<5.0.0',
 'xmltodict>=0.13.0,<0.14.0',
 'zarr>=2.14.0,<3.0.0']

extras_require = \
{'baby': ['aliby-baby>=0.1.17,<0.2.0'], 'omero': ['omero-py>=5.6.2']}

entry_points = \
{'console_scripts': ['aliby-annotate = aliby.bin.annotate:annotate',
                     'aliby-run = aliby.bin.run:run',
                     'aliby-visualise = aliby.bin.visualise:napari_overlay']}

setup_kwargs = {
    'name': 'aliby',
    'version': '0.1.64',
    'description': 'Process and analyse live-cell imaging data',
    'long_description': '# ALIBY (Analyser of Live-cell Imaging for Budding Yeast)\n\n[![docs](https://readthedocs.org/projects/aliby/badge/?version=master)](https://aliby.readthedocs.io/en/latest)\n[![PyPI version](https://badge.fury.io/py/aliby.svg)](https://badge.fury.io/py/aliby)\n[![pipeline](https://gitlab.com/aliby/aliby/badges/master/pipeline.svg?key_text=master)](https://gitlab.com/aliby/aliby/-/pipelines)\n[![dev pipeline](https://gitlab.com/aliby/aliby/badges/dev/pipeline.svg?key_text=dev)](https://gitlab.com/aliby/aliby/-/commits/dev)\n[![coverage](https://gitlab.com/aliby/aliby/badges/dev/coverage.svg)](https://gitlab.com/aliby/aliby/-/commits/dev)\n\nEnd-to-end processing of cell microscopy time-lapses. ALIBY automates segmentation, tracking, lineage predictions, post-processing and report production. It leverages the existing Python ecosystem and open-source scientific software available to produce seamless and standardised pipelines.\n\n## Quickstart Documentation\nInstallation of [VS Studio](https://visualstudio.microsoft.com/downloads/#microsoft-visual-c-redistributable-for-visual-studio-2022) Native MacOS support for is under work, but you can use containers (e.g., Docker, Podman) in the meantime.\n\nTo analyse local data\n ```bash\npip install aliby \n ```\n Add any of the optional flags `omero` and `utils` (e.g., `pip install aliby[omero, utils]`). `omero` provides tools to connect with an OMERO server and `utils` provides visualisation, user interface and additional deep learning tools.\n  \nSee our [installation instructions]( https://aliby.readthedocs.io/en/latest/INSTALL.html ) for more details.\n\n### CLI\n\nIf installed via poetry, you have access to a Command Line Interface (CLI)\n\n ```bash\naliby-run --expt_id EXPT_PATH --distributed 4 --tps None\n ```\n\nAnd to run Omero servers, the basic arguments are shown:\n ```bash\n aliby-run --expt_id XXX --host SERVER.ADDRESS --user USER --password PASSWORD \n ```\n\nThe output is a folder with the original logfiles and a set of hdf5 files, one with the results of each multidimensional inside.\n\nFor more information, including available options, see the page on [running the analysis pipeline](https://aliby.readthedocs.io/en/latest/PIPELINE.html)\n\n## Using specific components\n\n### Access raw data\n\nALIBY\'s tooling can also be used as an interface to OMERO servers, for example, to fetch a brightfield channel.\n ```python\nfrom aliby.io.omero import Dataset, Image\n\nserver_info= {\n            "host": "host_address",\n            "username": "user",\n            "password": "xxxxxx"}\nexpt_id = XXXX\ntps = [0, 1] # Subset of positions to get.\n\nwith Dataset(expt_id, **server_info) as conn:\n    image_ids = conn.get_images()\n\n#To get the first position\nwith Image(list(image_ids.values())[0], **server_info) as image:\n    dimg = image.data\n    imgs = dimg[tps, image.metadata["channels"].index("Brightfield"), 2, ...].compute()\n    # tps timepoints, Brightfield channel, z=2, all x,y\n```\n\n### Tiling the raw data\n\nA `Tiler` object performs trap registration. It may be built in different ways but the simplest one is using an image and a the default parameters set.\n\n```python\nfrom aliby.tile.tiler import Tiler, TilerParameters\nwith Image(list(image_ids.values())[0], **server_info) as image:\n    tiler = Tiler.from_image(image, TilerParameters.default())\n    tiler.run_tp(0)\n```\n\nThe initialisation should take a few seconds, as it needs to align the images\nin time.\n\nIt fetches the metadata from the Image object, and uses the TilerParameters values (all Processes in aliby depend on an associated Parameters class, which is in essence a dictionary turned into a class.)\n\n#### Get a timelapse for a given tile (remote connection)\n```python\nfpath = "h5/location"\n\ntile_id = 9\ntrange = range(0, 10)\nncols = 8\n\nriv = remoteImageViewer(fpath)\ntrap_tps = [riv.tiler.get_tiles_timepoint(tile_id, t) for t in trange] \n\n# You can also access labelled traps\nm_ts = riv.get_labelled_trap(tile_id=0, tps=[0])\n\n# And plot them directly\nriv.plot_labelled_trap(trap_id=0, channels=[0, 1, 2, 3], trange=range(10))\n```\n\nDepending on the network speed can take several seconds at the moment.\nFor a speed-up: take fewer z-positions if you can.\n\n#### Get the tiles for a given time point\nAlternatively, if you want to get all the traps at a given timepoint:\n\n```python\ntimepoint = (4,6)\ntiler.get_tiles_timepoint(timepoint, channels=None,\n                                z=[0,1,2,3,4])\n```\n\n\n### Contributing\nSee [CONTRIBUTING](https://aliby.readthedocs.io/en/latest/INSTALL.html) on how to help out or get involved.\n',
    'author': 'Alan Munoz',
    'author_email': 'alan.munoz@ed.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
