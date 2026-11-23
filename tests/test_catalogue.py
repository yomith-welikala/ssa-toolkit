import json
from ssa_toolkit.catalogue import load_catalogue


good = {
    "OBJECT_NAME": "DEMO",
    "OBJECT_ID": "25544",
    "EPOCH": "2019-12-09T16:38:29.000000",
    "MEAN_MOTION": 15.50103472,
    "ECCENTRICITY": 0.0007417,
    "INCLINATION": 51.6439,
    "RA_OF_ASC_NODE": 211.2001,
    "ARG_OF_PERICENTER": 17.6667,
    "MEAN_ANOMALY": 85.6398,
    "EPHEMERIS_TYPE": 0,
    "CLASSIFICATION_TYPE": "U",
    "NORAD_CAT_ID": 25544,
    "ELEMENT_SET_NO": 999,
    "REV_AT_EPOCH": 20248,
    "BSTAR": 3.8792e-05,
    "MEAN_MOTION_DOT": 1.764e-05,
    "MEAN_MOTION_DDOT": 0,
}
MissingKey = {
    "OBJECT_NAME": "DEMO",
    "OBJECT_ID": "2",
    "EPOCH": "2019-12-09T16:38:29.000000",
    "MEAN_MOTION": 15.50103472,
    "ECCENTRICITY": 0.0007417,
    "INCLINATION": 51.6439,
    "RA_OF_ASC_NODE": 211.2001,
    "ARG_OF_PERICENTER": 17.6667,
    "MEAN_ANOMALY": 85.6398,
    "EPHEMERIS_TYPE": 0,
    "CLASSIFICATION_TYPE": "U",
    "NORAD_CAT_ID": 2,
    "ELEMENT_SET_NO": 999,
    "REV_AT_EPOCH": 20248,
    "MEAN_MOTION_DOT": 1.764e-05,
    "MEAN_MOTION_DDOT": 0,
}
BadEpoch = {**good, "NORAD_CAT_ID": 3, "EPOCH": "garbage"}
UnphysicalOrbit = {**good, "NORAD_CAT_ID": 4, "ECCENTRICITY": 1.5}


def write_catalogue(tmp_path):
    f = tmp_path / "cat.json"
    f.write_text(json.dumps([good, MissingKey, BadEpoch, UnphysicalOrbit]))
    return f


def test_counts(tmp_path):
    f = write_catalogue(tmp_path)
    sats, ids, failures = load_catalogue(f)
    assert len(sats) == 1
    assert len(failures) == 3
    assert len(sats) + len(failures) == 4


def test_failure_reasons(tmp_path):
    f = write_catalogue(tmp_path)
    sats, ids, failures = load_catalogue(f)
    reason = dict(failures)
    assert ids == [25544]
    assert set(reason) == {2, 3, 4}
    assert "KeyError" in reason[2]
    assert "ValueError" in reason[3]
    assert "sgp4 error code" in reason[4]
