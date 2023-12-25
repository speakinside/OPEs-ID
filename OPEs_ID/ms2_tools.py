from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike

__all__ = ["is_mass_in"]


def close_in(x:ArrayLike, y:float, rtol:float=5e-6, atol:float=0) -> np.ndarray:
    """
    Calculates `y in x` for the float type within a tolerance.
    This function uses `numpy.isclose` to test equality, 
    hence using the following equation.

    absolute(`x` - `y`) <= (`atol` + `rtol` * absolute(`y`))

    Parameters
    ----------
    x : ArrayLike
        Input array
    y : float
        Test value.
    rtol : float, optional
        The relative tolerance parameter, by default 5e-6
    atol : float, optional
        The absolute tolerance parameter, by default 0

    Returns
    -------
    np.ndarray
        Test result.
    """
    return np.isclose(x, y, rtol=rtol, atol=atol).any()


_is_mass_in = np.vectorize(
    close_in, otypes=[bool], excluded=["y", "rtol", "atol"]
)


def is_mass_in(
    list_of_spec: Sequence[ArrayLike],
    test_mass: float,
    rtol: float = 5e-6,
    atol: float = 0,
) -> np.ndarray:
    """
    Returns a boolean array, where each element represents whether
    the corresponding m/z array in `list_of_spec` has `test_mass` within a tolerance.

    This function uses `numpy.isclose` to test equality, hence using the following equation.

    absolute(`x` - `test_mass`) <= (`atol` + `rtol` * absolute(`test_mass`))

    Parameters
    ----------
    list_of_spec : list of 1d array
        A list of m/z array.
    test_mass : float
        the targeted m/z value.
    rtol : float, optional
        The relative tolerance parameter (mass accuary), by default 5e-6
    atol : float, optional
        The absolute tolerance parameter, by default 0

    Returns
    -------
    np.ndarray
        Returns a boolean array, where each element represents whether
        the corresponding m/z array in `list_of_spec` has `test_mass` 
        within a tolerance.
    """
    return _is_mass_in(list_of_spec, test_mass, atol, rtol)
