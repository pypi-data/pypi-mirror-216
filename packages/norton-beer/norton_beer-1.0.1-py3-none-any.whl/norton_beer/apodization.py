#!/usr/bin/env python
""" Norton-Beer apodization window in spatial domain

This subpackage contains the generation of Norton-Beer apodization
window in spatial domain for any given set pf parameters. The Norton-Beer
apodization function class was firstly presented in [1]_ and [2]_.
Note, that the sum of the parameters must be equal to 1. Further,
if a float from [1.0, 1.1, 1.2, ..., 2.0], is given,
the parameters are used from [3]_.

This file is part of norton_beer.
"""
from norton_beer import __version__

__author__ = "Konstantin Ntokas"
__authors__ = ["Konstantin Ntokas", "Jörn Ungermann"]
__copyright__ = "Copyright (C) 2023, Konstantin Ntokas"
__license__ = "GNU Affero General Public License v3.0"
__version__ = __version__

import numpy as np
import logging


_LOG = logging.getLogger(__name__)

_NORTON_BEER_PARAMS = {
    1.0: np.array([1., 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    1.1: np.array([0.701551, -0.639244, 0.937693,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    1.2: np.array([0.396430, -0.150902, 0.754472,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    1.3: np.array([0.237413, -0.065285, 0.827872,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    1.4: np.array([0.153945, -0.141765, 0.987820,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    1.5: np.array([0.077112, 0.0, 0.703371, 0.0,
                   0.219517, 0.0, 0.0, 0.0, 0.0]),
    1.6: np.array([0.039234, 0.0, 0.630268, 0.0,
                   0.234934, 0.0, 0.095563, 0.0, 0.0]),
    1.7: np.array([0.020078, 0.0, 0.480667, 0.0,
                   0.386409, 0.0, 0.112845, 0.0, 0.0]),
    1.8: np.array([0.010172, 0.0, 0.344429, 0.0,
                   0.451817, 0.0, 0.193580, 0.0, 0.0]),
    1.9: np.array([0.004773, 0.0, 0.232473, 0.0,
                   0.464562, 0.0, 0.298191, 0.0, 0.0]),
    2.0: np.array([0.002267, 0.0, 0.140412, 0.0,
                   0.487172, 0.0, 0.256200, 0.0, 0.113948])
}


def norton_beer(N, par):
    """ This function generates the Norton-Beer apodization.

    Parameters
    ----------
    N : int
        number of samples
    par : float or 1darrray
        parameters of Norton-Beer apodization; if float is given,
        it must be one of [1.0, 1.1, ..., 2.0] and corresponds
        to the relative FWHM, which uses the published parameters in [3]_

    Returns
    -------
    apo : 1darray
        Norton-Beer apodization window

    Notes
    -----
    References of the Norton-Beer apodization function class
    are given in [1]_, [2]_ and [3]_
    """
    par = check_input(par)
    N_half = N // 2
    if N % 2 == 0:
        normv = 1.0 - ((np.arange(-N_half, N_half) + 0.5) / (N_half-0.5)) ** 2
    else:
        normv = 1.0 - (np.arange(-N_half, N_half+1) / N_half) ** 2
    apo = sum((a * (normv ** k) for (k, a) in enumerate(par)))
    return apo


def check_input(par):
    """ auxiliary function to assign FWHM to parameters, if given.

    Parameters
    ----------
    par : float or 1darrray
        parameters of Norton-Beer apodization; if float is given,
        it must be one of [1.0, 1.1, ..., 2.0] to use the predefined
        parameters from <_NORTON_BEER_PARAMS>

    Returns
    -------
    par : 1darray
        parameters of Norton-Beer apodization
    """

    if np.isscalar(par):
        if np.any(np.isclose(par, list(_NORTON_BEER_PARAMS.keys()))):
            par = _NORTON_BEER_PARAMS[par]
        elif par == 1:
            par = [par]
        else:
            _LOG.error("<par> for norton_beer apodization needs to one of "
                       "the scalar in the following list [1.1, 1.2, ..., 2.0]")
    else:
        if not np.isclose(np.sum(par), 1, atol=1e-3):
            _LOG.error("<par> for norton_beer apodization "
                       "needs to be an 1darray with sum 1")
    return par
