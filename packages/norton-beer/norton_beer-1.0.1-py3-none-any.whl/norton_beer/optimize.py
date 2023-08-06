#!/usr/bin/env python
""" Optimization to generation new apodization windows

This subpackage contains the generation of new Norton-Beer
apodization windows, where the spectral resolution of its
Fourier transform if fixed by the user and the parameters are
optimized so that the side lobes of the Fourier transform
are minimized. A wrapper function is available, which
optimizes the number of parameters needed.

This file is part of norton_beer.
"""
from norton_beer import __version__

__author__ = "Konstantin Ntokas"
__authors__ = ["Konstantin Ntokas", "Jörn Ungermann"]
__copyright__ = "Copyright (C) 2023, Konstantin Ntokas"
__license__ = "GNU Affero General Public License v3.0"
__version__ = __version__

import norton_beer.ils as ilsfun
import scipy.optimize as spop
import numpy as np
import logging
import norton_beer.apodization as apo


_LOG = logging.getLogger(__name__)


def boundary_line(fwhm):
    """ This function calculates the relative maximum values
    defined by the boundary line given by
    Norton and Beer (1976) doi: 10.1364/JOSA.66.000259

    Parameters
    ----------
    fwhm : float, ndarray
        full width at half maximum (FWHM) relative to sinc-function

    Returns
    -------
    float, ndarray
        absolute maximum  of side lobes relative to sinc-function
    """
    return 10**(1.939 - 1.401 * fwhm - 0.597 * fwhm**2)


def optimize_par(fwhm_want, nbpar, fac=500.):
    """ This function optimizes the parameters of Norton-Beer
    apodization for a given number of parameters and
    full width at half maximum (FWHM)


    Parameters
    ----------
    fwhm_want : float
        wanted relative full width at half maximum (FWHM)
    nbpar : int
        number of parameters
    fac : float, optional
        weight of fwhm difference in optimization;
        large values entails an optimized apodization
        which ILS's FWHM is close to the wanted FWHM, by default 500.

    Returns
    -------
    par : 1darray
        optimized parameters for Norton-Beer apodization
    fwhm : float
        full width at half maximum relative to sinc-function
    secmax : float
        absolute maximum  of side lobes relative to sinc-function
    """

    def objective_fun(par):
        ils = ilsfun.norton_beer(k, ifglen, par, check_input=False)
        _, fwhm, _, _ = ilsfun.calculate_fwhm(k, ils)
        _, secmax = ilsfun.calculate_secmax(ils)
        return fac * (fwhm_want - fwhm)**2 + secmax

    k = np.arange(-5, 5.001, 0.01)
    ifglen = 2

    # get starting values
    par = apo._NORTON_BEER_PARAMS[
        min(apo._NORTON_BEER_PARAMS.keys(),
            key=lambda key: abs(key - fwhm_want))
    ]
    par0 = np.zeros(nbpar)
    if len(par) < len(par0):
        par0[:len(par)] = par
    else:
        par0[:] = par[:len(par0)]

    # optimize parameter
    bound = nbpar * [(-1, 1)]
    cons = {'type': 'eq', 'fun': lambda x:  np.sum(x) - 1}
    res = spop.minimize(objective_fun, par0, bounds=bound,
                        constraints=cons, method="SLSQP")
    par = res.x

    # evaluate on optimized parameters
    ils = ilsfun.norton_beer(k, ifglen, par)
    _, fwhm, _, _ = ilsfun.calculate_fwhm(k, ils)
    _, secmax = ilsfun.calculate_secmax(ils)

    return par, fwhm, secmax


def optimize_nbpar(fwhm_want, fac=500.):
    """ This function finds the optimal number of parameters and
    returns the set of optimized parameters and the full width
    at half maximum (FWHM) (fwhm) and absolute maximum of the
    side lobe relative to sinc-function.

    Parameters
    ----------
    fwhm_want : float
        wanted relative full width at half maximum (FWHM)
    fac : float, optional
        weight of fwhm difference in optimization;
        large values entails an optimized apodization
        which ILS's FWHM is close to the wanted FWHM, by default 500.

    Returns
    -------
    par : 1darray
        optimized parameters for Norton-Beer apodization
    fwhm : float
        full width at half maximum (FWHM) relative to sinc-function
    secmax : float
        absolute maximum of side lobes relative to sinc-function
    """
    nbpars = np.arange(3, 11)
    fwhms = np.zeros(len(nbpars))
    secmaxs = np.zeros(len(nbpars))
    pars = []
    for i, nbpar in enumerate(nbpars):
        par, fwhms[i], secmaxs[i] = optimize_par(fwhm_want, nbpar, fac=fac)
        pars.append(par)
    idx = np.argmin(secmaxs)
    par, fwhm, secmax = pars[idx], fwhms[idx], secmaxs[idx]

    if abs(fwhm - fwhm_want) > 1e-2:
        _LOG.warning(f"FWHM ({fwhm:.2f}) deviates from "
                     f"FWHM want ({fwhm_want:.2f}).")

    # check if result is below boundary line
    secmax_bound = boundary_line(fwhm)
    if secmax > secmax_bound:
        _LOG.warning(f"ILS with {nbpar} optimized parameters lies above the "
                     f"boundary line for {fwhm:.2f}; secmax of ils: "
                     f"{secmax:.2e}, secmax of boundary line: "
                     f"{secmax_bound:.2e}")

    return par, fwhm, secmax
