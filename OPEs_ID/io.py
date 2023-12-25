import math
from collections import namedtuple

import numpy as np
import pandas as pd
import pymzml

from .defines import ColumnNames as C
from .mtype import ProgressFunc, check_progress


def load_mzml(
        filepath: str,
        load_ms1=True,
        load_ms2=True,
        progress: bool | ProgressFunc = True,
        **pymzml_kwargs,
):
    run = pymzml.run.Reader(filepath, **pymzml_kwargs)  # type: ignore
    ms1 = []
    ms2 = []

    progress = check_progress(progress)

    for spec in progress(run, total=run.get_spectrum_count()):
        mslevel = spec.ms_level
        mz = spec.mz
        int_ = spec.i
        rt = spec.scan_time_in_minutes() * 60
        sortarg = mz.argsort()
        mz = mz[sortarg]
        int_ = int_[sortarg]

        if mslevel == 1 and load_ms1:
            ms1.append((rt, mz, int_))
        elif mslevel == 2 and load_ms2:
            (precursor,) = spec.selected_precursors
            ms2.append((rt, precursor["mz"], precursor["i"], precursor.get("charge", math.nan), mz, int_))
    if load_ms1:
        ms1 = pd.DataFrame(ms1, columns=[C.RT, C.SpecMZ, C.SpecINT])

        ms1.sort_values(C.RT, inplace=True, ignore_index=True)
        ms1.index.name = C.MS1IDX
    else:
        ms1 = None
    if load_ms2:
        ms2 = pd.DataFrame(
            ms2,
            columns=[
                C.RT,
                C.PrecursorMZ,
                C.PrecursorInt,
                C.Charge,
                C.SpecMZ,
                C.SpecINT,
            ],
        )
        ms2.sort_values(C.RT, inplace=True, ignore_index=True)
        ms2.index.name = C.MS2IDX
    else:
        ms2 = None
    if load_ms1 and load_ms2:
        def find_int_in_ms1(ms2_s, ms1):
            ms1_s = ms1.loc[ms2_s[C.MS1IDX], [C.SpecMZ, C.SpecINT]]
            return ms1_s[C.SpecINT][
                np.argmin(np.abs(ms2_s[C.PrecursorMZ] - ms1_s[C.SpecMZ]))
            ]

        ms2[C.MS1IDX] = ms1[C.RT].searchsorted(ms2[C.RT]) - 1
        ms2.insert(
            3, C.PrecursorMS1Int, ms2.apply(find_int_in_ms1, axis=1, args=(ms1,))
        )
        ms1[C.ProductsIDX] = [
            ms2.index[ms2[C.MS1IDX] == idx].to_list() for idx in ms1.index
        ]

    return ms1, ms2
