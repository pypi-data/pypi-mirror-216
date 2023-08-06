import typing as t

import bottleneck as bn
import h5py
import numpy as np
import pandas as pd

from agora.abc import ParametersABC, StepABC
from agora.io.cells import Cells
from agora.io.writer import Writer, load_attributes
from aliby.tile.tiler import Tiler
from extraction.core.functions.defaults import exparams_from_meta
from extraction.core.functions.distributors import reduce_z, trap_apply
from extraction.core.functions.loaders import (
    load_custom_args,
    load_funs,
    load_redfuns,
)

# define types
reduction_method = t.Union[t.Callable, str, None]
extraction_tree = t.Dict[
    str, t.Dict[reduction_method, t.Dict[str, t.Collection]]
]
extraction_result = t.Dict[
    str, t.Dict[reduction_method, t.Dict[str, t.Dict[str, pd.Series]]]
]

# Global variables used to load functions that either analyse cells or their background. These global variables both allow the functions to be stored in a dictionary for access only on demand and to be defined simply in extraction/core/functions.
CELL_FUNS, TRAPFUNS, FUNS = load_funs()
CUSTOM_FUNS, CUSTOM_ARGS = load_custom_args()
RED_FUNS = load_redfuns()

# Assign datatype depending on the metric used
# m2type = {"mean": np.float32, "median": np.ubyte, "imBackground": np.ubyte}


class ExtractorParameters(ParametersABC):
    """Base class to define parameters for extraction."""

    def __init__(
        self,
        tree: extraction_tree,
        sub_bg: set = set(),
        multichannel_ops: t.Dict = {},
    ):
        """
        Initialise.

        Parameters
        ----------
        tree: dict
            Nested dictionary indicating channels, reduction functions and
            metrics to be used.
            str channel -> U(function, None) reduction -> str metric
            If not of depth three, tree will be filled with None.
        sub_bg: set
        multichannel_ops: dict
        """
        self.tree = tree
        self.sub_bg = sub_bg
        self.multichannel_ops = multichannel_ops

    @classmethod
    def default(cls):
        return cls({})

    @classmethod
    def from_meta(cls, meta):
        return cls(**exparams_from_meta(meta))


class Extractor(StepABC):
    """
    Apply a metric to cells identified in the tiles.

    Using the cell masks, the Extractor applies a metric, such as area or median, to cells identified in the image tiles.

    Its methods require both tile images and masks.

    Usually the metric is applied to only a tile's masked area, but some metrics depend on the whole tile.

    Extraction follows a three-level tree structure. Channels, such as GFP, are the root level; the reduction algorithm, such as maximum projection, is the second level; the specific metric, or operation, to apply to the masks, such as mean, is the third level.
    """

    # TODO Alan: Move this to a location with the SwainLab defaults
    default_meta = {
        "pixel_size": 0.236,
        "z_size": 0.6,
        "spacing": 0.6,
    }

    def __init__(
        self,
        parameters: ExtractorParameters,
        store: t.Optional[str] = None,
        tiler: t.Optional[Tiler] = None,
    ):
        """
        Initialise Extractor.

        Parameters
        ----------
        parameters: core.extractor Parameters
            Parameters that include the channels, reduction and
            extraction functions.
        store: str
            Path to the h5 file containing the cell masks.
        tiler: pipeline-core.core.segmentation tiler
            Class that contains or fetches the images used for segmentation.
        """
        self.params = parameters
        if store:
            self.local = store
            self.load_meta()
        else:
            # if no h5 file, use the parameters directly
            self.meta = {"channel": parameters.to_dict()["tree"].keys()}
        if tiler:
            self.tiler = tiler
        self.load_funs()

    @classmethod
    def from_tiler(
        cls,
        parameters: ExtractorParameters,
        store: str,
        tiler: Tiler,
    ):
        """Initiate from a tiler instance."""
        return cls(parameters, store=store, tiler=tiler)

    @classmethod
    def from_img(
        cls,
        parameters: ExtractorParameters,
        store: str,
        img_meta: tuple,
    ):
        """Initiate from images."""
        return cls(parameters, store=store, tiler=Tiler(*img_meta))

    @property
    def channels(self):
        """Get a tuple of the available channels."""
        if not hasattr(self, "_channels"):
            if type(self.params.tree) is dict:
                self._channels = tuple(self.params.tree.keys())
        return self._channels

    @property
    def current_position(self):
        return str(self.local).split("/")[-1][:-3]

    @property
    def group(self):
        """Return path within the h5 file."""
        if not hasattr(self, "_out_path"):
            self._group = "/extraction/"
        return self._group

    def load_custom_funs(self):
        """
        Incorporate the extra arguments of custom functions into their definitions.

        Normal functions only have cell_masks and trap_image as their
        arguments, and here custom functions are made the same by
        setting the values of their extra arguments.

        Any other parameters are taken from the experiment's metadata and automatically applied. These parameters therefore must be loaded within an Extractor instance.
        """
        # find functions specified in params.tree
        funs = set(
            [
                fun
                for ch in self.params.tree.values()
                for red in ch.values()
                for fun in red
            ]
        )
        # consider only those already loaded from CUSTOM_FUNS
        funs = funs.intersection(CUSTOM_FUNS.keys())
        # find their arguments
        self._custom_arg_vals = {
            k: {k2: self.get_meta(k2) for k2 in v}
            for k, v in CUSTOM_ARGS.items()
        }
        # define custom functions
        self._custom_funs = {}
        for k, f in CUSTOM_FUNS.items():

            def tmp(f):
                # pass extra arguments to custom function
                # return a function of cell_masks and trap_image
                return lambda cell_masks, trap_image: trap_apply(
                    f,
                    cell_masks,
                    trap_image,
                    **self._custom_arg_vals.get(k, {}),
                )

            self._custom_funs[k] = tmp(f)

    def load_funs(self):
        """Define all functions, including custum ones."""
        self.load_custom_funs()
        self._all_cell_funs = set(self._custom_funs.keys()).union(CELL_FUNS)
        # merge the two dicts
        self._all_funs = {**self._custom_funs, **FUNS}

    def load_meta(self):
        """Load metadata from h5 file."""
        self.meta = load_attributes(self.local)

    def get_tiles(
        self,
        tp: int,
        channels: t.Optional[t.List[t.Union[str, int]]] = None,
        z: t.Optional[t.List[str]] = None,
        **kwargs,
    ) -> t.Optional[np.ndarray]:
        """
        Find tiles for a given time point, channels, and z-stacks.

        Any additional keyword arguments are passed to tiler.get_tiles_timepoint

        Parameters
        ----------
        tp: int
            Time point of interest.
        channels: list of strings (optional)
            Channels of interest.
        z: list of integers (optional)
            Indices for the z-stacks of interest.
        """
        if channels is None:
            # find channels from tiler
            channel_ids = list(range(len(self.tiler.channels)))
        elif len(channels):
            # a subset of channels was specified
            channel_ids = [self.tiler.get_channel_index(ch) for ch in channels]
        else:
            # a list of the indices of the z stacks
            channel_ids = None
        if z is None:
            # gets the tiles data via tiler
            z = list(range(self.tiler.shape[-3]))
        res = (
            self.tiler.get_tiles_timepoint(
                tp, channels=channel_ids, z=z, **kwargs
            )
            if channel_ids
            else None
        )
        # data arranged as (tiles, channels, time points, X, Y, Z)
        return res

    def extract_traps(
        self,
        traps: t.List[np.ndarray],
        masks: t.List[np.ndarray],
        metric: str,
        labels: t.Dict[int, t.List[int]],
    ) -> t.Tuple[t.Union[t.Tuple[float], t.Tuple[t.Tuple[int]]]]:
        """
        Apply a function to a whole position.

        Parameters
        ----------
        traps: list of arrays
            t.List of images.
        masks: list of arrays
            t.List of masks.
        metric: str
            Metric to extract.
        labels: dict
            A dict of cell labels with trap_ids as keys and a list of cell labels as values.
        pos_info: bool
            Whether to add the position as an index or not.

        Returns
        -------
        res_idx: a tuple of tuples
            A two-tuple comprising a tuple of results and a tuple of the tile_id and cell labels
        """
        if labels is None:
            self._log("No labels given. Sorting cells using index.")
        cell_fun = True if metric in self._all_cell_funs else False
        idx = []
        results = []
        for trap_id, (mask_set, trap, lbl_set) in enumerate(
            zip(masks, traps, labels.values())
        ):
            # ignore empty traps
            if len(mask_set):
                # apply metric either a cell function or otherwise
                result = self._all_funs[metric](mask_set, trap)
                if cell_fun:
                    # store results for each cell separately
                    for lbl, val in zip(lbl_set, result):
                        results.append(val)
                        idx.append((trap_id, lbl))
                else:
                    # background (trap) function
                    results.append(result)
                    idx.append(trap_id)
        res_idx = (tuple(results), tuple(idx))
        return res_idx

    def extract_funs(
        self,
        traps: t.List[np.array],
        masks: t.List[np.array],
        metrics: t.List[str],
        **kwargs,
    ) -> t.Dict[str, pd.Series]:
        """
        Return dict with metrics as key and metrics applied to data as values.

        Data from one time point is used.
        """
        d = {
            metric: self.extract_traps(
                traps=traps, masks=masks, metric=metric, **kwargs
            )
            for metric in metrics
        }
        return d

    def reduce_extract(
        self,
        traps: np.ndarray,
        masks: t.List[np.ndarray],
        red_metrics: t.Dict[reduction_method, t.Collection[str]],
        **kwargs,
    ) -> t.Dict[str, t.Dict[reduction_method, t.Dict[str, pd.Series]]]:
        """
        Wrapper to apply reduction and then extraction.

        Parameters
        ----------
        tiles_data: array
            An array of image data arranged as (tiles, X, Y, Z)
        masks: list of arrays
            An array of masks for each trap: one per cell at the trap
        red_metrics: dict
            dict for which keys are reduction functions and values are either a list or a set of strings giving the metric functions.
            For example: {'np_max': {'max5px', 'mean', 'median'}}
        **kwargs: dict
            All other arguments passed to Extractor.extract_funs.

        Returns
        ------
        Dict of dataframes with the corresponding reductions and metrics nested.
        """
        # create dict with keys naming the reduction in the z-direction and the reduced data as values
        reduced_tiles_data = {}
        if traps is not None:
            for red_fun in red_metrics.keys():
                reduced_tiles_data[red_fun] = [
                    self.reduce_dims(tile_data, method=RED_FUNS[red_fun])
                    for tile_data in traps
                ]
        d = {
            red_fun: self.extract_funs(
                metrics=metrics,
                traps=reduced_tiles_data.get(red_fun, [None for _ in masks]),
                masks=masks,
                **kwargs,
            )
            for red_fun, metrics in red_metrics.items()
        }
        return d

    def reduce_dims(
        self, img: np.ndarray, method: reduction_method = None
    ) -> np.ndarray:
        """
        Collapse a z-stack into 2d array using method.

        If method is None, return the original data.

        Parameters
        ----------
        img: array
            An array of the image data arranged as (X, Y, Z).
        method: function
            The reduction function.
        """
        reduced = img
        if method is not None:
            reduced = reduce_z(img, method)
        return reduced

    def extract_tp(
        self,
        tp: int,
        tree: t.Optional[extraction_tree] = None,
        tile_size: int = 117,
        masks: t.Optional[t.List[np.ndarray]] = None,
        labels: t.Optional[t.List[int]] = None,
        **kwargs,
    ) -> t.Dict[str, t.Dict[str, t.Dict[str, tuple]]]:
        """
        Extract for an individual time point.

        Parameters
        ----------
        tp : int
            Time point being analysed.
        tree : dict
            Nested dictionary indicating channels, reduction functions and
            metrics to be used.
            For example: {'general': {'None': ['area', 'volume', 'eccentricity']}}
        tile_size : int
            Size of the tile to be extracted.
        masks : list of arrays
            A list of masks per trap with each mask having dimensions (ncells, tile_size,
            tile_size).
        labels : dict
            A dictionary with trap_ids as keys and cell_labels as values.
        **kwargs : keyword arguments
            Passed to extractor.reduce_extract.

        Returns
        -------
        d: dict
            Dictionary of the results with three levels of dictionaries.
            The first level has channels as keys.
            The second level has reduction metrics as keys.
            The third level has cell or background metrics as keys and a two-tuple as values.
            The first tuple is the result of applying the metrics to a particular cell or trap; the second tuple is either (trap_id, cell_label) for a metric applied to a cell or a trap_id for a metric applied to a trap.

            An example is d["GFP"]["np_max"]["mean"][0], which gives a tuple of the calculated mean GFP fluorescence for all cells.
        """
        # TODO Can we split the different extraction types into sub-methods to make this easier to read?
        if tree is None:
            # use default
            tree: extraction_tree = self.params.tree
        # dictionary with channel: {reduction algorithm : metric}
        ch_tree = {ch: v for ch, v in tree.items() if ch != "general"}
        # tuple of the channels
        tree_chs = (*ch_tree,)
        # create a Cells object to extract information from the h5 file
        cells = Cells(self.local)
        # find the cell labels and store as dict with trap_ids as keys
        if labels is None:
            raw_labels = cells.labels_at_time(tp)
            labels = {
                trap_id: raw_labels.get(trap_id, [])
                for trap_id in range(cells.ntraps)
            }
        # find the cell masks for a given trap as a dict with trap_ids as keys
        if masks is None:
            raw_masks = cells.at_time(tp, kind="mask")
            masks = {trap_id: [] for trap_id in range(cells.ntraps)}
            for trap_id, cells in raw_masks.items():
                if len(cells):
                    masks[trap_id] = np.stack(np.array(cells)).astype(bool)
        # convert to a list of masks
        masks = [np.array(v) for v in masks.values()]
        # find image data at the time point
        # stored as an array arranged as (traps, channels, time points, X, Y, Z)
        tiles = self.get_tiles(tp, tile_shape=tile_size, channels=tree_chs)
        # generate boolean masks for background as a list with one mask per trap
        bgs = np.array([])
        if self.params.sub_bg:
            bgs = ~np.array(
                list(
                    map(
                        lambda x: np.sum(x, axis=0)
                        if np.any(x)
                        else np.zeros((tile_size, tile_size)),
                        masks,
                    )
                )
            ).astype(bool)
        # perform extraction by applying metrics
        d = {}
        self.img_bgsub = {}
        for ch, red_metrics in tree.items():
            # NB ch != is necessary for threading
            if ch != "general" and tiles is not None and len(tiles):
                # image data for all traps and z sections for a particular channel
                # as an array arranged as (tiles, Z, X, Y, )
                img = tiles[:, tree_chs.index(ch), 0]
            else:
                img = None
            # apply metrics to image data
            d[ch] = self.reduce_extract(
                traps=img,
                masks=masks,
                red_metrics=red_metrics,
                labels=labels,
                **kwargs,
            )
            # apply metrics to image data with the background subtracted
            if bgs.any() and ch in self.params.sub_bg and img is not None:
                # calculate metrics with subtracted bg
                ch_bs = ch + "_bgsub"
                # subtract median background

                self.img_bgsub[ch_bs] = np.moveaxis(
                    np.stack(
                        list(
                            map(
                                lambda tile, mask: np.moveaxis(tile, 0, -1)
                                - bn.median(tile[:, mask], axis=1),
                                img,
                                bgs,
                            )
                        )
                    ),
                    -1,
                    1,
                )  # End with tiles, z, y, x
                # apply metrics to background-corrected data
                d[ch_bs] = self.reduce_extract(
                    red_metrics=ch_tree[ch],
                    traps=self.img_bgsub[ch_bs],
                    masks=masks,
                    labels=labels,
                    **kwargs,
                )
        # apply any metrics using multiple channels, such as pH calculations
        for name, (
            chs,
            merge_fun,
            red_metrics,
        ) in self.params.multichannel_ops.items():
            if len(
                set(chs).intersection(
                    set(self.img_bgsub.keys()).union(tree_chs)
                )
            ) == len(chs):
                channels_stack = np.stack(
                    [self.get_imgs(ch, tiles, tree_chs) for ch in chs], axis=-1
                )
                merged = RED_FUNS[merge_fun](channels_stack, axis=-1)
                d[name] = self.reduce_extract(
                    red_metrics=red_metrics,
                    traps=merged,
                    masks=masks,
                    labels=labels,
                    **kwargs,
                )
        return d

    def get_imgs(self, channel: t.Optional[str], tiles, channels=None):
        """
        Return image from a correct source, either raw or bgsub.

        Parameters
        ----------
        channel: str
            Name of channel to get.
        tiles: ndarray
            An array of the image data having dimensions of (tile_id, channel, tp, tile_size, tile_size, n_zstacks).
        channels: list of str (optional)
            t.List of available channels.

        Returns
        -------
        img: ndarray
            An array of image data with dimensions (no tiles, X, Y, no Z channels)
        """
        if channels is None:
            channels = (*self.params.tree,)
        if channel in channels:  # TODO start here to fetch channel using regex
            return tiles[:, channels.index(channel), 0]
        elif channel in self.img_bgsub:
            return self.img_bgsub[channel]

    def _run_tp(
        self,
        tps: t.List[int] = None,
        tree=None,
        save=True,
        **kwargs,
    ) -> dict:
        """
        Wrapper to add compatibility with other steps of the pipeline.

        Parameters
        ----------
        tps: list of int (optional)
            Time points to include.
        tree: dict (optional)
            Nested dictionary indicating channels, reduction functions and
            metrics to be used.
            For example: {'general': {'None': ['area', 'volume', 'eccentricity']}}
        save: boolean (optional)
            If True, save results to h5 file.
        kwargs: keyword arguments (optional)
            Passed to extract_tp.

        Returns
        -------
        d: dict
            A dict of the extracted data with a concatenated string of channel, reduction metric, and cell metric as keys and pd.Series of the extracted data as values.
        """
        if tree is None:
            tree = self.params.tree
        if tps is None:
            tps = list(range(self.meta["time_settings/ntimepoints"][0]))
        elif isinstance(tps, int):
            tps = [tps]
        # store results in dict
        d = {}
        for tp in tps:
            # extract for each time point and convert to dict of pd.Series
            new = flatten_nesteddict(
                self.extract_tp(tp=tp, tree=tree, **kwargs),
                to="series",
                tp=tp,
            )
            # concatenate with data extracted from early time points
            for k in new.keys():
                d[k] = pd.concat((d.get(k, None), new[k]), axis=1)
        # add indices to pd.Series containing the extracted data
        for k in d.keys():
            indices = ["experiment", "position", "trap", "cell_label"]
            idx = (
                indices[-d[k].index.nlevels :]
                if d[k].index.nlevels > 1
                else [indices[-2]]
            )
            d[k].index.names = idx
        # save
        if save:
            self.save_to_hdf(d)
        return d

    def save_to_hdf(self, dict_series, path=None):
        """
        Save the extracted data to the h5 file.

        Parameters
        ----------
        dict_series: dict
            A dictionary of the extracted data, created by run.
        path: Path (optional)
            To the h5 file.
        """
        if path is None:
            path = self.local
        self.writer = Writer(path)
        for extract_name, series in dict_series.items():
            dset_path = "/extraction/" + extract_name
            self.writer.write(dset_path, series)
        self.writer.id_cache.clear()

    def get_meta(self, flds: t.Union[str, t.Collection]):
        """Obtain metadata for one or multiple fields."""
        if isinstance(flds, str):
            flds = [flds]
        meta_short = {k.split("/")[-1]: v for k, v in self.meta.items()}
        return {
            f: meta_short.get(f, self.default_meta.get(f, None)) for f in flds
        }


### Helpers
def flatten_nesteddict(
    nest: dict, to="series", tp: int = None
) -> t.Dict[str, pd.Series]:
    """
    Convert a nested extraction dict into a dict of pd.Series.

    Parameters
    ----------
    nest: dict of dicts
        Contains the nested results of extraction.
    to: str (optional)
        Specifies the format of the output, either pd.Series (default) or a list
    tp: int
        Time point used to name the pd.Series

    Returns
    -------
    d: dict
        A dict with a concatenated string of channel, reduction metric, and cell metric as keys and either a pd.Series or a list of the corresponding extracted data as values.
    """
    d = {}
    for k0, v0 in nest.items():
        for k1, v1 in v0.items():
            for k2, v2 in v1.items():
                d["/".join((k0, k1, k2))] = (
                    pd.Series(*v2, name=tp) if to == "series" else v2
                )
    return d


class hollowExtractor(Extractor):
    """
    Extractor that only cares about receiving images and masks.

    Used for testing.
    """

    def __init__(self, parameters):
        self.params = parameters
