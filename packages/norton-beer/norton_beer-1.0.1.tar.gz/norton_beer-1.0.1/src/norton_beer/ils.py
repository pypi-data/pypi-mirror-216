#!/usr/bin/env python
""" ILS of Norton-Beer apodization window in spectral domain

This subpackage contains the generation of the analytical
Fourier transform of the Norton-Beer apodization in spectral
domain for any given set pf parameters. The Norton-Beer
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
import math
import norton_beer.apodization as apo
from scipy.signal import find_peaks
import logging


_LOG = logging.getLogger(__name__)
_SINC_FWHM = 0.6033540716481244
_SINC_SECMAX = 0.21723186696037824


def norton_beer(k, ifglen, par, check_input=True):
    """ This function creates the analytical Fourier Transform
    of the Norton-Beer apodization.

    Parameters
    ----------
    k : 1darray
        spectral axis
    ifglen : float
        signal length
    par : float or 1darrray
        parameters of Norton-Beer apodization; if float is given,
        it must be one of [1.0, 1.1, ..., 2.0] and corresponds
        to the relative FWHM, which uses the published parameters in [3]_
    check_input : bool, optional
        if True, input is modified for 2 things;
        firstly, if float is given for <par>,
        predefined parameters presented by
        Naylor and Tahic 2007 are used; secondly,
        it is checked weather sum over parameters
        is equal to one

    Returns
    -------
    result : 1darray
        Fourier transform of Norton-Beer apodization window

    Notes
    -----
    References of the Norton-Beer apodization function class
    are given in [1]_, [2]_ and [3]_.
    """

    def calc_q_fac(N):
        sinc_fac = np.zeros((N, N))
        sinc_fac[0, 0] = 1
        cos_fac = np.zeros((N, N))

        # recursive calcuation of the factors
        for m in range(1, N):
            sinc_fac[m, 0] = 1
            sinc_fac[m, 1:] = 2*m * (2*m-1) * sinc_fac[m-1, :-1]

            cos_fac[m, 1] = 2*m
            cos_fac[m, 2:] = 2*m * (2*m-1) * cos_fac[m-1, 1:-1]

        # account for negative values
        fac_neg = np.ones(N)
        fac_neg[::2] = -1
        sinc_fac *= -fac_neg[np.newaxis, :]
        cos_fac *= fac_neg[np.newaxis, :]

        # calculate outer sum with binomial coeff.
        fac_sinc_mx = np.zeros((N, N))
        fac_cos_mx = np.zeros((N, N))
        for n in range(N):
            fac = np.array([
                math.comb(n, m) * (-1)**m for m in range(n+1)
            ])[:, np.newaxis]
            fac_sinc_mx[n, :] = np.sum(sinc_fac[:n+1, :] * fac, axis=0)
            fac_cos_mx[n, :] = np.sum(cos_fac[:n+1, :] * fac, axis=0)

        # calculate factor when taylor expansion is applied
        bound = max(N, 5)
        K = 2 * bound
        idx0 = np.tile(np.arange(K), N)
        idx1 = np.repeat(np.arange(N), K)
        factorial0 = np.array(
            [math.factorial(2 * idx) for idx in idx0]
        ).astype(float)
        factorial1 = np.array(
            [math.factorial(2 * idx + 1) for idx in idx0]
        ).astype(float)
        fac_taylor = ((-1)**idx0[np.newaxis, :] * (
            fac_sinc_mx[:, idx1] / factorial1[np.newaxis, :] +
            fac_cos_mx[:, idx1] / factorial0[np.newaxis, :]
            ))
        fac_apow = (2 * idx0 - 2 * idx1).astype(int)

        fac_apow_uni = np.unique(fac_apow)
        for pow in fac_apow_uni[fac_apow_uni < 0]:
            assert np.allclose(
                np.sum(fac_taylor[:, fac_apow == pow], axis=1), 0.
            )
        fac_taylor_mx = np.zeros((N, bound))
        for i, pow in enumerate(2 * np.arange(bound)):
            fac_taylor_mx[:, i] = np.sum(
                fac_taylor[:, fac_apow == pow],
                axis=1
            )

        return fac_sinc_mx, fac_cos_mx, fac_taylor_mx

    ils = np.zeros_like(k)
    a = np.pi * k * ifglen
    if check_input:
        par = apo.check_input(par)
    par = np.trim_zeros(par, trim="b")

    # get factors
    sinc_mx, cos_mx, taylor_mx = calc_q_fac(len(par))

    # case 1: if a < 1 -> analytical solution unstable -> expansion
    mask = abs(a) < 1
    apower = np.zeros((taylor_mx.shape[1], len(a[mask])))
    apower[0, :] = 1
    apower[1, :] = a[mask]**2
    for i in range(2, apower.shape[0]):
        apower[i, :] = apower[i-1, :] * apower[1, :]
    qns = np.matmul(taylor_mx, apower)
    ils[mask] = np.sum(par[:, np.newaxis] * qns, axis=0)

    # case 2: if a >= 1 -> analytical solution
    sinca, cosa = np.sinc(a[~mask] / np.pi), np.cos(a[~mask])
    apower = np.zeros((sinc_mx.shape[1], len(a[~mask])))
    apower[0, :] = 1
    if apower.shape[0] > 1:
        apower[1, :] = a[~mask]**2
    if apower.shape[0] > 2:
        for i in range(2, apower.shape[0]):
            apower[i, :] = apower[i-1, :] * apower[1, :]
    apower_inv = 1 / apower
    qns = (np.matmul(sinc_mx, apower_inv) * sinca +
           np.matmul(cos_mx, apower_inv) * cosa)
    ils[~mask] = np.sum(par[:, np.newaxis] * qns, axis=0)

    return ils


def norton_beer_numerical(k, ifglen, par, nb_sample=100001):
    """ This function generates the ILS numerically
    via discrete Fourier Transform.

    Parameters
    ----------
    k : 1darray
        spectral axis
    ifglen : float
        signal length
    par : float or 1darray
        parameters of Norton-Beer apodization
    nb_samples : int, optional
        number of samples, should be odd, by default 100001

    Returns
    -------
    ils : 1darray
        numerical Fourier transformation of
        Norton-Beer apodization window
    ils_x : 1darray
        corresponding spectral axis; should
        be close to <k>
    """

    par = apo.check_input(par)

    # many samples such that error between
    # numerical and analytical ILS decreases
    k_step = round(abs(k[0] - k[1]), 10)
    dx = ifglen / nb_sample
    n_pad = int(round(1 / (k_step * dx), 0))
    assert n_pad >= nb_sample

    # generate ILS via FFT
    apo_spat = apo.norton_beer(nb_sample, par)

    # zero padding
    if (n_pad % 2 != 0) & (nb_sample % 2 != 0):
        start = (n_pad - nb_sample) // 2
    elif (n_pad % 2 == 0) & (nb_sample % 2 != 0):
        start = (n_pad - nb_sample) // 2 + 1
    end = n_pad - start - nb_sample
    apo_spat = np.pad(apo_spat, (start, end))

    # get Fourier transform of apodization function
    apo_spat = np.fft.ifftshift(apo_spat, axes=-1)
    ils = np.fft.fft(apo_spat) / nb_sample
    ils_x = np.fft.fftfreq(n_pad, d=dx)
    ils = np.fft.fftshift(ils)
    ils_x = np.fft.fftshift(ils_x)
    assert not np.any(abs(np.imag(ils)) > 1e-10)
    ils = np.real(ils)

    # cut at range of original x-axis
    idx = (ils_x >= k[0] - k_step/2) & (ils_x <= k[-1] + k_step/2)
    ils = ils[idx]
    ils_x = ils_x[idx]

    return ils, ils_x


def lin_interp(x, y, i, half):
    """ This function does linear interpolation between two values
    at position <index> and <index>+1.

    Parameters
    ----------
    x : 1darry
        abscissa
    y : 1darray
        ordinate
    i : int
        index
    half : float
        half of maximal value

    Returns
    -------
    float
        interpolated value of x-axis at half of maximal value
    """

    return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))


def calculate_fwhm(x, y):
    """ This function calculates the full width at half maximum (FWHM)
    relative to sinc-function.

    Parameters
    ----------
    x : 1darry
        abscissa
    y : 1darray
        ordinate

    Returns
    -------
    fwhm : float
        full width at half maximum
    range_fwhm : array-like with two entries
        start and end of FWHM on x-axis
    half : float
        half of maximal value
    """

    half = np.max(y) / 2
    argmax = np.argmax(y)

    # find lower index
    i_low = argmax
    while y[i_low] > half:
        i_low -= 1
        if i_low == -1:
            _LOG.debug("No fwhm found. Lower part does "
                       "not fall below half maximum.")
            return np.nan, np.nan, np.nan
    # find upper index
    i_up = argmax
    len_y = len(y)
    while y[i_up] > half:
        i_up += 1
        if i_up == len_y:
            _LOG.debug("No fwhm found. Upper part does "
                       "not fall below half maximum.")
            return np.nan, np.nan, np.nan
    i_up -= 1

    range_fwhm = np.zeros(2)
    if hasattr(x, "units"):
        range_fwhm *= x.units
    range_fwhm[0] = lin_interp(x, y, i_low, half)
    range_fwhm[1] = lin_interp(x, y, i_up, half)
    fwhm = range_fwhm[1] - range_fwhm[0]

    return fwhm, fwhm / _SINC_FWHM, range_fwhm, half


def calculate_secmax(y):
    """ This function calculates the maximal value
    of side lobes relative to sinc-function


    Parameters
    ----------
    y : 1darray
        ordinate

    Returns
    -------
    secmax : float
        absolute maximum of side lobes
    secmax_rel : float
        absolute maximum of side lobes relative to sinc
    """
    y = abs(y)
    idx_peaks = find_peaks(y)[0]
    sorted_peaks = np.sort(y[idx_peaks])
    secmax = sorted_peaks[-3]
    secmax /= y.max()
    secmax_rel = secmax / _SINC_SECMAX
    return secmax, secmax_rel
