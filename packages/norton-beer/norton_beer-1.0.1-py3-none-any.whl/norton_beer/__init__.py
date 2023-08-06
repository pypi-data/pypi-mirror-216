"""
norton_beer
===========
The 'norton_beer' library is a python tool box for
the Norton-Beer apodization functions.

Provides:
    1. Norton-Beer apodization window generation in spatial domain
    2. the analytical Fourier transform of the apodization window
       also known as instrument line shape (ILS)
    3. generation of new apodization window for a fixed spatial
       resolution of the ILS so that the sides lobes are minimized

Installation
------------

To use norton_beer, first install it using pip:

.. code-block:: console

   pip install norton-beer

Testing
-------

To test the `norton_beer` package, clone the repository from github
(https://github.com/konstntokas/norton_beer) and run:

.. code-block:: console

   pytest

Note that pytest needs to be installed on the local machine.

Available modules
-----------------
apodization
    generation of apodization window in spatial domain
ils
    generation of ILS in spectral domain
optimize
    generation of new apodizations for a fixed spatial
    resolution of the ILS so that the sides lobes are minimized

Further references
------------------
.. [1] Norton, R. H., & Beer, R. (1976). New apodizing functions
    for Fourier spectrometry. Journal of the Optical Society of America,
    66 (3), 259. https://doi.org/10.1364/JOSA.66.000259
.. [2] Norton, R. H., & Beer, R. (1977). Errata: New Apodizing
    Functions For Fourier Spectrometry. Journal of the Optical Society
    of America, 67 (3), 419. https://doi.org/10.1364/JOSA.67.000419
.. [3] Naylor, D. A., & Tahic, M. K. (2007). Apodizing functions
    for Fourier transform spectroscopy. Journal of the Optical Society
    of America A, 24 (11), 3644.260 https://doi.org/10.1364/JOSAA.24.003644
"""
import pkg_resources

__author__ = "Konstantin Ntokas"
__authors__ = ["Konstantin Ntokas", "Jörn Ungermann"]
__copyright__ = "Copyright 2023, Konstantin Ntokas"
__license__ = "GNU Affero General Public License v3.0"
__version__ = pkg_resources.get_distribution(__name__).version

from . import apodization
from . import ils
from . import optimize


__all__ = ['apodization', 'ils', 'optimize']
