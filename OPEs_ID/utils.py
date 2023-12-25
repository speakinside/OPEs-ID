import inspect
from collections.abc import MappingView, Sized, Iterable

import joblib
import numpy as np
import pandas as pd

from .mtype import ProgressFunc, check_progress


def rbf(x, center, sigma):
    # norm = 1 / (np.sqrt(2*np.pi)*sigma)
    return np.exp(-np.square((x - center)) / (2 * sigma**2))


class ProgressParallel(joblib.Parallel):
    __doc__ = joblib.Parallel.__doc__

    def __init__(self, *args, **kwargs):
        sig = inspect.signature(super().__init__)
        bind_sig = sig.bind(*args, **kwargs)
        bind_sig.apply_defaults()
        if bind_sig.arguments["return_as"] == "list":
            self.__return_list = True
            bind_sig.arguments["return_as"] = "generator"
        super().__init__(*bind_sig.args, **bind_sig.kwargs)

    def __call__(self, iterable: Iterable, progress: ProgressFunc | bool = True):
        """Main function to dispatch parallel tasks.

        Parameters
        ----------
        iterable : Iterable
            `joblib.delayed` functions.
        progress : ProgressFunc | bool, optional
            If True, show progress using `tqdm.tqdm`.If False, show nothing.
            Optionally, passing a `ProgressFunc` like object will update progress using this object,
            by default True.

        Returns
        -------
        list | Iterable
            results.
        """
        total = None
        if isinstance(iterable, Sized):
            total = len(iterable)
        progress = check_progress(progress)
        iterator = progress(super().__call__(iterable), total=total)
        if self.__return_list:
            return list(iterator)
        else:
            return iterator


class DictTuple(MappingView):
    def __init__(self, tup, col) -> None:
        self.tup = tup
        self.col = col

    def __getitem__(self, key):
        if not isinstance(key, int):
            key = self.col.index(key)
        return self.tup[key]

    def __len__(self) -> int:
        return len(self.tup)

    def tuple(self):
        return self.tup

    def __repr__(self) -> str:
        return repr(self.tup)

    def __str__(self) -> str:
        return str(self.tup)


@pd.api.extensions.register_dataframe_accessor("dtuple")
class DictNamedTuple:
    def __init__(self, pandas_object: pd.DataFrame) -> None:
        self.pd_obj = pandas_object

    def iter(self, index=True, name="Pandas"):
        if index:
            col = ["Index"]
        else:
            col = []
        col.extend(self.pd_obj.columns)
        for tup in self.pd_obj.itertuples(index=index, name=name):
            yield DictTuple(tup, col)
