from heinlein import load_dataset
from astropy.coordinates import SkyCoord
import astropy.units as u

hsc = load_dataset("hsc")
center = SkyCoord(141.23246, 2.32358, unit="deg")
radius = 120*u.arcsec


data = hsc.cone_search(center, radius, dtypes=["catalog", "mask"])
cat = data["catalog"]
mask = data["mask"]

print(cat)
print(cat[mask])