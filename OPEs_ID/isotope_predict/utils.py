import itertools

import numpy as np

from OPEs_ID.elements import EDB, Element
from OPEs_ID.utils import rbf


def lstq_rbf(int_candi, int_std, int_sigma):
    int_candi = np.asarray(int_candi)
    k = np.inner(int_candi, int_std) / np.inner(
        int_candi, int_candi
    )
    delta = int_std - int_candi * k
    return rbf(delta, 0, int_sigma).min()


def make_isotope_grid(isotopes_grid: dict[str | Element, list[int]]):
    grid = {}
    for iso, lst in isotopes_grid.items():
        if isinstance(iso, str):
            iso = EDB[iso]
            if not isinstance(iso, Element):
                raise ValueError()
        grid[iso] = lst.copy()
    keys, values = zip(*grid.items())
    for v in itertools.product(*values):
        params = dict(zip(keys, v))
        if all(v == 0 for v in params.values()):
            continue
        yield params


def get_isotopes_dist(isotopes: dict[Element, int], atol=None, rtol=None, rtol_base=0):
    isotopes = isotopes.copy()
    for k in list(isotopes.keys()):
        if isotopes[k] == 0:
            del isotopes[k]
    all_aw, all_dist, all_names = zip(
        *[ele.isotopes_distribution(n) for (ele, n) in isotopes.items()])
    atomic_weight = np.asarray([np.sum(aw)
                                for aw in itertools.product(*all_aw)])
    distribution = np.asarray([np.prod(dist)
                               for dist in itertools.product(*all_dist)])
    names = np.asarray([np.sum(name)
                        for name in itertools.product(*all_names)])
    sort = atomic_weight.argsort()
    atomic_weight = atomic_weight[sort]
    distribution = distribution[sort]
    names = names[sort]
    if atol is None and rtol is None:
        return atomic_weight, distribution, names
    merged_aw = []
    merged_dist = []
    merged_names = []
    visited = np.zeros_like(atomic_weight, bool)
    for i in range(visited.size):
        if not visited[i]:
            sel = True
            if atol is not None:
                sel &= np.abs(atomic_weight - atomic_weight[i]) < atol
            if rtol is not None:
                sel &= np.abs(
                    atomic_weight - atomic_weight[i]) / ((atomic_weight + atomic_weight[i]) / 2 + rtol_base) < rtol
            merged_aw.append(atomic_weight[sel].mean())
            merged_dist.append(distribution[sel].prod())
            merged_names.append(names[sel][0])
            visited[sel] = True
    return np.array(merged_aw), np.array(merged_dist), np.array(merged_names, dtype=object)


def reverse_search_for_isotopes(ms2_mz,
                                ms2_int,
                                ms1_mz,
                                ms1_int,
                                isotopes_grid: dict[str | Element, list[int]],
                                mass_acc=5e-6,
                                top_n=5,
                                intensity_sigma=0.1,
                                atol=None,
                                rtol=None,
                                rtol_base=0,
                                ):
    results = []
    for isotopes_comb in make_isotope_grid(isotopes_grid):
        atomic_weight, distribution, names = get_isotopes_dist(
            isotopes_comb, atol=atol, rtol=rtol, rtol_base=rtol_base)
        distribution /= distribution.max()
        if top_n is not None:
            top_idx = np.argsort(distribution)[-top_n:]
            atomic_weight = atomic_weight[top_idx]
            distribution = distribution[top_idx]
            names = names[top_idx]

        for i in range(atomic_weight.size):

            mass_diff = np.delete(atomic_weight, i) - atomic_weight[i]
            combines = [[ms2_int]]
            for mz_diff in mass_diff:
                mz_min = (1 - mass_acc) * (
                        ms2_mz / (1 + mass_acc) + mz_diff
                )
                mz_max = (1 + mass_acc) * (
                        ms2_mz / (1 - mass_acc) + mz_diff
                )
                combines.append(
                    ms1_int[(mz_min <= ms1_mz) & (ms1_mz <= mz_max)].ravel())

            candidates = tuple(itertools.product(*combines))
            if len(candidates) != 0:
                std_int = np.concatenate(
                    (distribution[i], np.delete(distribution, i)), axis=None)
                p = max([lstq_rbf(int_candi, std_int, intensity_sigma)
                         for int_candi in candidates])
                results.append((p, names[i]))
    r = max(results, default=None, key=lambda x: x[0])
    if r is None or r[0] < 0.8:
        return None
    else:
        return r
