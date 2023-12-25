import dataclasses
import functools
import itertools
import operator
from collections import namedtuple
from typing import Literal, Optional, Sequence

import numpy as np
import pandas as pd
import tqdm


from .mtype import ProgressFunc, check_progress
from .defines import ColumnNames as C
from .elements import EDB
from .expr import ChemFormula

MS1Ion = namedtuple("MS1Ion", ["MS1_IDX", "RT", "MZ", "INT"])


@dataclasses.dataclass
class TargetIon:
    formula: ChemFormula
    smarts: str
    type: Optional[Literal["Aryl", "Alkyl"]] = None
    refname: Optional[str] = None

    def __post_init__(self):
        if self.refname is None:
            self.refname = self.formula.empirical_formula(show_isotope=False)

    @property
    def mass(self):
        return self.formula.mass

    # To support unpacking
    def __len__(self):
        return 3

    def __getitem__(self, idx):
        fs = dataclasses.fields(self)
        return getattr(self, fs[idx].name)


def isotope_distribution(
    elements: dict[str, int],
    normalize_mass: Optional[Literal["highest", "first", "last"]] = None,
    normalize_distribution: bool = False,
):
    mass = []
    distribution = []
    names = []
    for ele, num in elements.items():
        iso_weights, iso_dists, iso_names = EDB[ele].isotopes_distribution(num)
        mass.append(iso_weights)
        distribution.append(iso_dists)
        names.append(iso_names)

    mass = np.asarray([np.sum(item) for item in itertools.product(*mass)])
    distribution = np.asarray(
        [np.prod(item) for item in itertools.product(*distribution)]
    )
    names = np.asarray(
        [functools.reduce(operator.add, item) for item in itertools.product(*names)],
        dtype=object,
    )  # type: ignore
    if normalize_distribution:
        distribution /= distribution.max()

    if normalize_mass == "highest":
        mass -= mass[distribution.argmax()]
    elif normalize_mass == "first":
        mass -= mass.min()
    elif normalize_mass == "last":
        mass -= mass.max()

    order = np.argsort(mass)
    mass = mass[order]
    distribution = distribution[order]
    names = names[order]
    return mass, distribution, names


def get_closest_ion(mz, ms1mz, ms1int):
    mz_idx = np.abs(mz - ms1mz).argmin()
    return ms1mz[mz_idx], ms1int[mz_idx]


def ms2_ms1_roi(ms2, ms1, mass_deviation, progress: ProgressFunc | bool = True):
    progress = check_progress(progress)

    roi_id = pd.Series(-1, index=ms2.index, dtype=int, name=C.ROIGroupID)
    roi_idx_counter = 0
    ms2_idx_to_ms1_roi = {}

    for idx in progress(roi_id.index):
        if roi_id.at[idx] == -1:
            current_roi_idx = roi_idx_counter
            roi_idx_counter += 1

            roi_id.at[idx] = current_roi_idx
            mz_list = [ms2.at[idx, C.PrecursorMZ]]
            ms1_idx_start = ms2.at[idx, C.MS1IDX]

            p = ms1_idx_start
            spec = ms1.loc[p]
            m, i = get_closest_ion(
                ms2.at[idx, C.PrecursorMZ], spec[C.SpecMZ], spec[C.SpecINT]
            )
            roi_ms1 = [MS1Ion(p, ms1.at[p, "RT"], m, i)]
            # forward:
            while p < ms1.index.max():
                mz_mean = np.mean(mz_list)
                p += 1
                spec = ms1.loc[p]
                ms2_hit = (ms2[C.MS1IDX] == p) & np.isclose(
                    ms2[C.PrecursorMZ], mz_mean, rtol=mass_deviation, atol=0
                )

                if ms2_hit.any():
                    roi_id[ms2_hit] = current_roi_idx
                    mz_list.extend(ms2.loc[ms2_hit, C.PrecursorMZ].to_list())
                else:
                    e = np.abs(spec[C.SpecMZ] - mz_mean)
                    if np.any(e <= mz_mean * mass_deviation):
                        mz_list.append(spec[C.SpecMZ][np.argmin(e)])
                    else:
                        break
                m, i = get_closest_ion(mz_mean, spec[C.SpecMZ], spec[C.SpecINT])
                roi_ms1.append(MS1Ion(p, ms1.at[p, C.RT], m, i))

            p = ms1_idx_start
            # backward:
            while p > ms1.index.min():
                mz_mean = np.mean(mz_list)
                p -= 1
                spec = ms1.loc[p]
                ms2_hit = (ms2[C.MS1IDX] == p) & np.isclose(
                    ms2[C.PrecursorMZ], mz_mean, rtol=mass_deviation, atol=0
                )

                if ms2_hit.any():
                    roi_id[ms2_hit] = current_roi_idx
                    mz_list.extend(ms2.loc[ms2_hit, C.PrecursorMZ].to_list())
                else:
                    e = np.abs(spec[C.SpecMZ] - mz_mean)
                    if np.any(e <= mz_mean * mass_deviation):
                        mz_list.append(spec[C.SpecMZ][np.argmin(e)])
                    else:
                        break
                m, i = get_closest_ion(mz_mean, spec[C.SpecMZ], spec[C.SpecINT])
                roi_ms1.append(MS1Ion(p, ms1.at[p, C.RT], m, i))
            ms2_idx_to_ms1_roi[current_roi_idx] = pd.DataFrame(roi_ms1)
    df = pd.concat((ms2[C.PrecursorMS1Int], roi_id), axis=1)
    return df, ms2_idx_to_ms1_roi


def eic(target_mz, ms1, rtol=5e-6, atol=0):
    def _f(s):
        sel_int = s[C.SpecINT][np.isclose(s[C.SpecMZ], target_mz, rtol=rtol, atol=atol)]
        return sel_int.sum()

    tic_int = ms1[[C.SpecMZ, C.SpecINT]].apply(_f, axis=1)
    return pd.DataFrame(data={C.RT: ms1[C.RT], "EIC_INT": tic_int})


def search_from_another_ms1(target_mz, rt, ms1, mass_acc, rt_atol=1):
    eic_df = eic(target_mz, ms1, mass_acc)
    sel = np.logical_and(eic_df[C.RT] > (rt - rt_atol), eic_df[C.RT] < (rt + rt_atol))
    return eic_df.loc[sel, "EIC_INT"].max()
