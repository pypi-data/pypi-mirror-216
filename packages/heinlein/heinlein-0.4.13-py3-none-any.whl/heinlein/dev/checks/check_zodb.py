from heinlein import load_project
from heinlein import load_dataset, Region
import astropy.units as u
import numpy as np


project = load_project("sl2s-troubleshoot")
weights = project.get("weights")[0]
coords = project.get("coords-to-check")
region_mask = project.get("region-mask")
value_mask = project.get("value-mask")

los_to_check = weights[region_mask][value_mask]
print("got the data!")
cfht = load_dataset("cfht")
fractions = np.zeros(len(coords))
for i, c in enumerate(coords):
    if (i%25 == 0):
        print(f"Complete {i} of {len(fractions)}")
    r = Region.circle(c, 120*u.arcsec)
    f = cfht.mask_fraction(r)
    fractions[i] = f

project.check_in("mask-fractions", fractions)