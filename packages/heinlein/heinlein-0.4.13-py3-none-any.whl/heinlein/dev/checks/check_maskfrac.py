from shapely import geometry
from heinlein import  Region
from heinlein import load_dataset
import astropy.units as u
import time

hsc  = load_dataset("cfht")

hsc_center = (33.61786584, -5.30368409)
reg = Region.circle(hsc_center, 120*u.arcsec)
a = hsc.mask_fraction(reg)


data = hsc.cone_search(hsc_center, 120*u.arcsec, dtypes=["catalog", "mask"])
print(data)
cat = data['catalog']
mask = data['mask']
masked_cat = cat[mask]
import matplotlib.pyplot as plt
plt.plot(cat['ra'], cat['dec'], c="red")
plt.plot(masked_cat['ra'], masked_cat['dec'], c="blue")
plt.show()

print(a