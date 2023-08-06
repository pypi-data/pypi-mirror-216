# ALIBY (Analyser of Live-cell Imaging for Budding Yeast)

[![docs](https://readthedocs.org/projects/aliby/badge/?version=master)](https://aliby.readthedocs.io/en/latest)
[![PyPI version](https://badge.fury.io/py/aliby.svg)](https://badge.fury.io/py/aliby)
[![pipeline](https://gitlab.com/aliby/aliby/badges/master/pipeline.svg?key_text=master)](https://gitlab.com/aliby/aliby/-/pipelines)
[![dev pipeline](https://gitlab.com/aliby/aliby/badges/dev/pipeline.svg?key_text=dev)](https://gitlab.com/aliby/aliby/-/commits/dev)
[![coverage](https://gitlab.com/aliby/aliby/badges/dev/coverage.svg)](https://gitlab.com/aliby/aliby/-/commits/dev)

End-to-end processing of cell microscopy time-lapses. ALIBY automates segmentation, tracking, lineage predictions, post-processing and report production. It leverages the existing Python ecosystem and open-source scientific software available to produce seamless and standardised pipelines.

## Quickstart Documentation
Installation of [VS Studio](https://visualstudio.microsoft.com/downloads/#microsoft-visual-c-redistributable-for-visual-studio-2022) Native MacOS support for is under work, but you can use containers (e.g., Docker, Podman) in the meantime.

To analyse local data
 ```bash
pip install aliby 
 ```
 Add any of the optional flags `omero` and `utils` (e.g., `pip install aliby[omero, utils]`). `omero` provides tools to connect with an OMERO server and `utils` provides visualisation, user interface and additional deep learning tools.
  
See our [installation instructions]( https://aliby.readthedocs.io/en/latest/INSTALL.html ) for more details.

### CLI

If installed via poetry, you have access to a Command Line Interface (CLI)

 ```bash
aliby-run --expt_id EXPT_PATH --distributed 4 --tps None
 ```

And to run Omero servers, the basic arguments are shown:
 ```bash
 aliby-run --expt_id XXX --host SERVER.ADDRESS --user USER --password PASSWORD 
 ```

The output is a folder with the original logfiles and a set of hdf5 files, one with the results of each multidimensional inside.

For more information, including available options, see the page on [running the analysis pipeline](https://aliby.readthedocs.io/en/latest/PIPELINE.html)

## Using specific components

### Access raw data

ALIBY's tooling can also be used as an interface to OMERO servers, for example, to fetch a brightfield channel.
 ```python
from aliby.io.omero import Dataset, Image

server_info= {
            "host": "host_address",
            "username": "user",
            "password": "xxxxxx"}
expt_id = XXXX
tps = [0, 1] # Subset of positions to get.

with Dataset(expt_id, **server_info) as conn:
    image_ids = conn.get_images()

#To get the first position
with Image(list(image_ids.values())[0], **server_info) as image:
    dimg = image.data
    imgs = dimg[tps, image.metadata["channels"].index("Brightfield"), 2, ...].compute()
    # tps timepoints, Brightfield channel, z=2, all x,y
```

### Tiling the raw data

A `Tiler` object performs trap registration. It may be built in different ways but the simplest one is using an image and a the default parameters set.

```python
from aliby.tile.tiler import Tiler, TilerParameters
with Image(list(image_ids.values())[0], **server_info) as image:
    tiler = Tiler.from_image(image, TilerParameters.default())
    tiler.run_tp(0)
```

The initialisation should take a few seconds, as it needs to align the images
in time.

It fetches the metadata from the Image object, and uses the TilerParameters values (all Processes in aliby depend on an associated Parameters class, which is in essence a dictionary turned into a class.)

#### Get a timelapse for a given tile (remote connection)
```python
fpath = "h5/location"

tile_id = 9
trange = range(0, 10)
ncols = 8

riv = remoteImageViewer(fpath)
trap_tps = [riv.tiler.get_tiles_timepoint(tile_id, t) for t in trange] 

# You can also access labelled traps
m_ts = riv.get_labelled_trap(tile_id=0, tps=[0])

# And plot them directly
riv.plot_labelled_trap(trap_id=0, channels=[0, 1, 2, 3], trange=range(10))
```

Depending on the network speed can take several seconds at the moment.
For a speed-up: take fewer z-positions if you can.

#### Get the tiles for a given time point
Alternatively, if you want to get all the traps at a given timepoint:

```python
timepoint = (4,6)
tiler.get_tiles_timepoint(timepoint, channels=None,
                                z=[0,1,2,3,4])
```


### Contributing
See [CONTRIBUTING](https://aliby.readthedocs.io/en/latest/INSTALL.html) on how to help out or get involved.
