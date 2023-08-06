"""
Description: This file tests the function in apodization.py.

:copyright: 2023 (for authors see AUTHORS file). All rights reserved.
"""

import norton_beer.apodization as apo
import numpy as np
import json
from pathlib import Path
import os


def test_apodization():
    """
    Tests the function apodization
    """

    _DIR = Path(__file__).resolve().parent
    files = ["spatial_even.json", "spatial_odd.json"]
    for file in files:
        with open(os.path.join(_DIR, file), "rb") as json_file:
            dat = json.load(json_file)
        for (k, v) in dat.items():
            res = apo.norton_beer(len(v), float(k))
            assert np.allclose(res, np.asarray(v)), f"{file} {k}"
