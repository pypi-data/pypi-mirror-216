from heinlein import load_project
from pathlib import Path

path = Path("cleanup.py")
project = load_project("test5")
project.check_in("test_path_2", path, overwrite=True)
g = project.get("test_path_2")
print(g)