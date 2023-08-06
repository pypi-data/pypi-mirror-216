from astropy.coordinates import SkyCoord
from heinlein import load_dataset
import astropy.units as u
import matplotlib.pyplot as plt
from heinlein import Region

center = (34.83553657, -5.11219075)
sk = SkyCoord(*center, unit="deg")
r = Region.circle(sk, 120*u.arcsec)
cfht = load_dataset("cfht")
data = cfht.cone_search(sk, 120*u.arcsec, dtypes=["catalog", "mask"])
cat = data["catalog"]
mask = data["mask"]
grid = r.get_grid(100000)
g = mask.mask(grid)
print(g)
plt.scatter(g.ra, g.dec)
plt.show()
print(cfht.mask_fraction(r))