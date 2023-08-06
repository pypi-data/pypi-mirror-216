from heinlein import create_project, delete_project
import numpy as np



c = create_project("test5")
data = np.zeros((100,100))

print("checking in 1")
c.check_in("test", data)
print("checking in 2")
c.check_in("test_data.test", data)
print("done")