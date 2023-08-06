# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heinlein',
 'heinlein.api',
 'heinlein.config',
 'heinlein.config.datasets.support',
 'heinlein.dataset',
 'heinlein.dev.checks',
 'heinlein.dev.other',
 'heinlein.dtypes',
 'heinlein.dtypes.handlers',
 'heinlein.manager',
 'heinlein.project',
 'heinlein.region',
 'heinlein.tests.ptest',
 'heinlein.utilities']

package_data = \
{'': ['*'],
 'heinlein': ['dev/*',
              'tests/project/*',
              'tests/project/403bc7e2-b6e8-11ed-96bb-8afecd8df53c/*',
              'tests/project/47c35fc0-b6e8-11ed-9c6a-8afecd8df53c/*',
              'tests/project/82b6979a-b6cb-11ed-b872-8afecd8df53c/*',
              'tests/project/82b6979a-b6cb-11ed-b872-8afecd8df53c/data/*',
              'tests/project/b2d91d2c-b6e8-11ed-ba1c-8afecd8df53c/*',
              'tests/project/data/*'],
 'heinlein.config': ['datasets/*', 'dtypes/*', 'project/*', 'region/*'],
 'heinlein.config.datasets.support': ['hsc_tiles/*'],
 'heinlein.dataset': ['configs/*', 'configs/configs_bkp/*']}

install_requires = \
['Shapely>=2.0.0,<3.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'astropy>=5.1,<6.0',
 'cacheout>=0.14.1,<0.15.0',
 'dynaconf>=3.1.9,<4.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'portalocker>=2.5.1,<3.0.0',
 'pymongo>=4.2.0,<5.0.0',
 'regions==0.7',
 'spherical-geometry>=1.2.22,<2.0.0']

entry_points = \
{'console_scripts': ['heinlein = heinlein.entrypoint:delegate_command']}

setup_kwargs = {
    'name': 'heinlein',
    'version': '0.4.13',
    'description': 'Library for interacting with large astronomical survey datasets',
    'long_description': 'None',
    'author': 'Patrick Wells',
    'author_email': 'pwells@ucdavis.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
