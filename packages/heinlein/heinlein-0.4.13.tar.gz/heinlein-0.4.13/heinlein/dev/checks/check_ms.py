from heinlein import load_dataset
from heinlein import Region
import astropy.units as u
import matplotlib.pyplot as plt
if __name__ == "__main__":
    radius = 120*u.arcsec
    ms = load_dataset("ms")
    ms.set_field((7,7))

    data = ms.cone_search((-1.75, -1.75), 120*u.arcsec)
    cat = data["catalog"]
    plt.scatter(cat['ra'], cat['dec'])
    plt.show()

    exit()

    g = ms.generate_grid(radius=120*u.arcsec, overlap = 1)

    for point in g:
        data = ms.cone_search(point, radius)
        print(data)