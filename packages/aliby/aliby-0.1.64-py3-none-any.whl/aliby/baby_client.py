"""
Underlying methods for different neural network deployments.
"""
import itertools
import logging
import re
import time
import typing as t
from pathlib import Path
from time import perf_counter

import baby.errors
import h5py
import numpy as np
import requests
from agora.abc import ParametersABC, StepABC
from baby import modelsets
from baby.brain import BabyBrain
from baby.crawler import BabyCrawler
from requests.exceptions import HTTPError, Timeout


################### Dask Methods ################################
def format_segmentation(segmentation, tp):
    """Format a single timepoint into a dictionary.

    Parameters
    ------------
    segmentation: list
                  A list of results, each result is the output of the crawler, which is JSON-encoded
    tp: int
        the time point considered

    Returns
    --------
    A dictionary containing the formatted results of BABY
    """
    # Segmentation is a list of dictionaries, ordered by trap
    # Add trap information
    # mother_assign = None
    for i, x in enumerate(segmentation):
        x["trap"] = [i] * len(x["cell_label"])
        x["mother_assign_dynamic"] = np.array(x["mother_assign"])[
            np.array(x["cell_label"], dtype=int) - 1
        ]
    # Merge into a dictionary of lists, by column
    merged = {
        k: list(itertools.chain.from_iterable(res[k] for res in segmentation))
        for k in segmentation[0].keys()
    }
    # Special case for mother_assign
    # merged["mother_assign_dynamic"] = [merged["mother_assign"]]
    if "mother_assign" in merged:
        del merged["mother_assign"]
    #     mother_assign = [x["mother_assign"] for x in segmentation]
    # Check that the lists are all of the same length (in case of errors in
    # BABY)
    n_cells = min([len(v) for v in merged.values()])
    merged = {k: v[:n_cells] for k, v in merged.items()}
    merged["timepoint"] = [tp] * n_cells
    # merged["mother_assign"] = mother_assign
    return merged


class BabyParameters(ParametersABC):
    def __init__(
        self,
        model_config: t.Dict[
            str, t.Union[str, int, float, bool, t.List[t.Union[int, float]]]
        ],
        tracker_params,
        clogging_thresh,
        min_bud_tps,
        isbud_thresh,
        session,
        graph,
        print_info,
        suppress_errors,
        error_dump_dir,
        tf_version: int,
    ):
        self.model_config = model_config
        self.tracker_params = tracker_params
        self.clogging_thresh = clogging_thresh
        self.min_bud_tps = min_bud_tps
        self.isbud_thresh = isbud_thresh
        self.session = session
        self.graph = graph
        self.print_info = print_info
        self.suppress_errors = suppress_errors
        self.error_dump_dir = error_dump_dir
        self.tf_version = tf_version

    @classmethod
    def default(cls, **kwargs):
        """kwargs passes values to the model chooser"""
        return cls(
            model_config=choose_model_from_params(**kwargs),
            tracker_params=dict(ctrack_params=dict(), budtrack_params=dict()),
            clogging_thresh=1,
            min_bud_tps=3,
            isbud_thresh=0.5,
            session=None,
            graph=None,
            print_info=False,
            suppress_errors=False,
            error_dump_dir=None,
            tf_version=2,
        )

    def update_baby_modelset(self, path: t.Union[str, Path, t.Dict[str, str]]):
        """
        Replace default BABY model and flattener with another one from a folder outputted
        by our standard retraining script.
        """

        if isinstance(path, dict):
            weights_flattener = {k: Path(v) for k, v in path.items()}
        else:
            weights_dir = Path(path)
            weights_flattener = {
                "flattener_file": weights_dir.parent / "flattener.json",
                "morph_model_file": weights_dir / "weights.h5",
            }

        self.update("model_config", weights_flattener)


class BabyRunner(StepABC):
    """A BabyRunner object for cell segmentation.

    Does segmentation one time point at a time."""

    def __init__(self, tiler, parameters=None, **kwargs):
        self.tiler = tiler
        # self.model_config = modelsets()[choose_model_from_params(**kwargs)]
        self.model_config = (
            choose_model_from_params(**kwargs)
            if parameters is None
            else parameters.model_config
        )

        tiler_z = self.tiler.shape[-3]
        model_name = self.model_config["flattener_file"]
        if tiler_z != 5:
            assert (
                f"{tiler_z}z" in model_name
            ), f"Tiler z-stack ({tiler_z}) and Model shape ({model_name}) do not match "

        self.brain = BabyBrain(**self.model_config)
        self.crawler = BabyCrawler(self.brain)
        self.bf_channel = self.tiler.ref_channel_index

    @classmethod
    def from_tiler(cls, parameters: BabyParameters, tiler):
        return cls(tiler, parameters)

    def get_data(self, tp):
        # Swap axes x and z, probably shouldn't swap, just move z
        return (
            self.tiler.get_tp_data(tp, self.bf_channel)
            .swapaxes(1, 3)
            .swapaxes(1, 2)
        )

    def _run_tp(self, tp, with_edgemasks=True, assign_mothers=True, **kwargs):
        """Simulating processing time with sleep"""
        # Access the image
        t = perf_counter()
        img = self.get_data(tp)
        segmentation = self.crawler.step(
            img,
            with_edgemasks=with_edgemasks,
            assign_mothers=assign_mothers,
            **kwargs,
        )
        return format_segmentation(segmentation, tp)


def choose_model_from_params(
    modelset_filter=None,
    camera="prime95b",
    channel="brightfield",
    zoom="60x",
    n_stacks="5z",
):
    """
    Define which model to query from the server based on a set of parameters.

    Parameters
    ----------
    modelset_filter: str
                    A regex filter to apply on the models to start.
    camera: str
            The camera used in the experiment (case insensitive).
    channel:str
            The channel used for segmentation (case insensitive).
    zoom: str
          The zoom on the channel.
    n_stacks: str
              The number of z_stacks to use in segmentation

    Returns
    -------
    model_name : str
    """
    valid_models = list(modelsets().keys())

    # Apply modelset filter if specified
    if modelset_filter is not None:
        msf_regex = re.compile(modelset_filter)
        valid_models = filter(msf_regex.search, valid_models)

    # Apply parameter filters if specified
    params = [
        str(x) if x is not None else ".+"
        for x in [camera.lower(), channel.lower(), zoom, n_stacks]
    ]
    params_re = re.compile("^" + "_".join(params) + "$")
    valid_models = list(filter(params_re.search, valid_models))
    # Check that there are valid models
    if len(valid_models) == 0:
        raise KeyError(
            "No model sets found matching {}".format(", ".join(params))
        )
    # Pick the first model
    return modelsets()[valid_models[0]]
