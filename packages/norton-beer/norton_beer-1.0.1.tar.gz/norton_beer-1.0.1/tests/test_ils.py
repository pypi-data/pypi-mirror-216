import numpy as np
import norton_beer.ils as ilsfun


def test_ils_analytical():
    """
    this function tests the analytical ils generation against
    the numerical ils generation for Norton-Beer
    """
    ifglen = 1.5
    pars = np.round(np.arange(1.1, 2.01, 0.1), 1)
    ils_xs = [
        np.arange(-10, 10, 0.1),
        np.arange(-10, 10.01, 0.1)
    ]
    tags = ["even", "odd"]

    for (ils_x, tag) in zip(ils_xs, tags):
        for par in pars:
            ilsn, ilsn_x = ilsfun.norton_beer_numerical(ils_x, ifglen, par)
            ilsa = ilsfun.norton_beer(ils_x, ifglen, par)
            assert np.allclose(ilsn_x, ils_x, atol=1e-5), f"ilsx, {tag}, {par}"
            assert np.allclose(ilsn, ilsa, atol=1e-5), f"ils, {tag}, {par}"


def test_lin_interp():
    """
    this function tests the function 'lin_interp'
    """

    x = np.arange(-5., 5.5)
    y = abs(x) / 5
    i = 1
    half = 0.75
    test = ilsfun.lin_interp(x, y, i, half)
    assert np.allclose(test, -3.75)


def test_calculate_fwhm():
    """
    this function tests the function 'calculate_fwhm'
    """
    x = np.arange(-5., 5.01, 0.0001)
    y = np.sinc(2 * x)
    fwhm, rel_fwhm, range_fwhm, half = ilsfun.calculate_fwhm(x, y)
    assert np.allclose(half, 0.5)
    assert np.allclose(
        range_fwhm,
        np.array([-0.5, 0.5]) * ilsfun._SINC_FWHM,
        atol=1e-6
    )
    assert np.allclose(fwhm, ilsfun._SINC_FWHM, atol=1e-6)
    assert np.allclose(rel_fwhm, 1, atol=1e-6)


def test_calculate_secmax():
    """
    this function tests the function 'calculate_secmax'
    """
    x = np.arange(-5., 5.01, 0.0001)
    y = np.sinc(2 * x)
    secmax, secmax_rel = ilsfun.calculate_secmax(y)
    assert np.allclose(secmax, ilsfun._SINC_SECMAX, atol=1e-6)
    assert np.allclose(secmax_rel, 1, atol=1e-6)
