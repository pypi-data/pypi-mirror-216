
from heinlein import load_dataset, Region
from shapely import geometry
import astropy.units as u
import matplotlib.pyplot as plt
des_center = (13.4349,-20.2091)
hsc_center = (141.23246, 2.32358)
cfht_center = (35.2, -6.4)
radius = 240*u.arcsecond

print("TESTING CFHT")
d = load_dataset("cfht")
a = d.cone_search(cfht_center, radius, dtypes=["catalog", "mask"])
print(a)

print("TESTING DES")
d = load_dataset("des")
a = d.cone_search(des_center, radius, dtypes=["catalog", "mask"])
print(a)

print("TESTING HSC")
d = load_dataset("hsc")
a = d.cone_search(hsc_center, radius, dtypes=["catalog", "mask"])
print(a)

