import pytest
from astropy.time import Time

from ssa_toolkit.timeconv import calendar_to_jd, tle_epoch_to_jd

TOL = 1e-3 / 86400

CALENDAR_CASES = [
    (2000, 1, 1, 0, 0, 0),
    (2020, 2, 29, 18, 30, 15.5),
    (2023, 12, 31, 23, 59, 59),
    (1998, 7, 4, 6, 15, 0),
    (2026, 1, 1, 0, 0, 0),
]

TLE_CASES = [
    (20060.5, 2020),
    (98200.25, 1998),
    (1.0, 2000),
    (24366.75, 2024),
    (99100.5, 1999),
]


@pytest.mark.parametrize("args", CALENDAR_CASES)
def test_calendar_to_jd(args):
    y, m, d, h, mi, s = args
    ref = Time(f"{y:04d}-{m:02d}-{d:02d}T{h:02d}:{mi:02d}:{s:06.3f}", scale="utc")
    my_jd, my_fr = calendar_to_jd(*args)
    diff = (my_jd - ref.jd1) + (my_fr - ref.jd2)
    assert abs(diff) < TOL


@pytest.mark.parametrize("epoch, year", TLE_CASES)
def test_tle_epoch_to_jd(epoch, year):
    ddd = int(epoch % 1000)
    frac = (epoch % 1000) - ddd
    ref = Time(f"{year}:{ddd:03d}:00:00:00", format="yday", scale="utc")
    my_jd, my_fr = tle_epoch_to_jd(epoch)
    diff = (my_jd - ref.jd1) + (my_fr - (ref.jd2 + frac))
    assert abs(diff) < TOL
