import tqdm
import pandas as pd
from .utils import reverse_search_for_isotopes
from ..mtype import ProgressFunc, check_progress
from typing import Callable, Iterable
from collections.abc import Sequence, Mapping
from ..elements import Element, EDB
from ..defines import ColumnNames as C


def check_isotope_params(parmas: Mapping[str | Element, Sequence]) -> dict[Element, list]:
    new_param = {}
    for ele, seq in parmas.items():
        if isinstance(ele, str):
            new_param[EDB[ele]] = list(seq)
        elif isinstance(ele, Element):
            new_param[ele] = list(seq)
        else:
            raise ValueError(f'Unsupported value "{ele}" of type "{ele.__class__}".')
    return new_param


def _ga(named_tup, name):
    return getattr(named_tup, name)


def predict_isotope(ms2: pd.DataFrame, ms1: pd.DataFrame, isotope_params: Mapping[str | Element, Sequence | set],
                    mass_acc=5e-6, top_n=5, *,
                    progress: ProgressFunc | bool = True):
    progress = check_progress(progress)
    isotope_params = check_isotope_params(isotope_params)
    isotope_predict = []
    for s in progress(ms2.itertuples(), total=ms2.shape[0]):
        ms1_mz = ms1.at[_ga(s, C.MS1IDX), C.SpecMZ]
        ms1_int = ms1.at[_ga(s, C.MS1IDX), C.SpecINT]
        r = reverse_search_for_isotopes(
            _ga(s, C.PrecursorMZ), _ga(s, C.PrecursorMS1Int), ms1_mz, ms1_int, isotope_params, mass_acc=mass_acc,
            top_n=top_n)
        isotope_predict.append(r)
    return isotope_predict
