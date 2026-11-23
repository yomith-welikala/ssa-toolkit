import json
from sgp4.api import Satrec
from sgp4 import omm


def load_catalogue(path):
    sats = []
    ids = []
    failures = []
    records = json.load(open(path))
    for rec in records:
        try:
            sat = Satrec()
            omm.initialize(sat, rec)
        except (KeyError, ValueError) as e:
            failures.append((rec.get("NORAD_CAT_ID"), f"{type(e).__name__}: {e}"))
            continue
        if sat.error != 0:
            failures.append((rec.get("NORAD_CAT_ID"), f"sgp4 error code {sat.error}"))
            continue
        sats.append(sat)
        ids.append(rec["NORAD_CAT_ID"])
    return sats, ids, failures


if __name__ == "__main__":
    sats, ids, failures = load_catalogue("data/active.json")
    print(len(sats), len(failures), failures[:3])
