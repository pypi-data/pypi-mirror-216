import numpy as np
import norton_beer.optimize as nbopt


def test_boundary_line():
    """
    this function tests the function 'boundary_line'
    """
    fwhm = 1.65
    test = nbopt.boundary_line(fwhm)
    assert np.allclose(test, 0.01004656272327508)


def test_optimize_par():
    """
    this function tests the function 'optimize_par'
    """
    fwhm_want = 1.7
    nbpar = 6
    par, fwhm, secmax = nbopt.optimize_par(fwhm_want, nbpar, fac=1000.)
    assert np.allclose(
        par,
        np.array([0.01824, 0.01239, 0.48838, -0.07074, 0.36210, 0.18961]),
        atol=1e-2
    )
    assert np.allclose(fwhm, 1.69996, atol=1e-5)
    assert np.allclose(secmax, 0.004970, atol=1e-5)


def test_optimize_nbpar():
    """
    this function tests the function 'optimize_nbpar'
    """
    fwhm_want = 1.7
    par, fwhm, secmax = nbopt.optimize_nbpar(fwhm_want, fac=1000.)
    assert np.allclose(
        par,
        np.array([0.01824, 0.01239, 0.48838, -0.07074, 0.36210, 0.18961]),
        atol=1e-2
    )
    assert np.allclose(fwhm, 1.69996, atol=1e-5)
    assert np.allclose(secmax, 0.004970, atol=1e-5)
