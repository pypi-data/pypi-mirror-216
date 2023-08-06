from astropy.coordinates import SkyCoord
import astropy.units as u
from heinlein import load_dataset, Region
import matplotlib.pyplot as plt
cfht = load_dataset("cfht")
center = SkyCoord(35.14915086, -6.27486393, unit="deg")
reg = Region.circle(center, 240*u.arcsec)
g = reg.get_grid(100000)
data = cfht.cone_search(center, 120*u.arcsec, dtypes=["catalog", "mask"])
mask = data["mask"]
g_ = mask.mask(g)
plt.scatter(g_.ra, g_.dec)
plt.scatter(data["catalog"]["ra"], data["catalog"]["dec"])
plt.scatter(center.ra, center.dec)
plt.show()