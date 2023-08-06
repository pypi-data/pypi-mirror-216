# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cellseg_gsontools',
 'cellseg_gsontools.geometry',
 'cellseg_gsontools.merging',
 'cellseg_gsontools.spatial_context',
 'cellseg_gsontools.summary']

package_data = \
{'': ['*']}

install_requires = \
['geopandas>=0.11.1,<0.12.0',
 'libpysal>=4.7.0,<5.0.0',
 'mapclassify>=2.5.0,<3.0.0',
 'matplotlib>=3.6.1,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'opencv-python>=4.2.0.32,<5.0.0.0',
 'pandarallel>=1.6.4,<2.0.0',
 'pathos>=0.2.9,<0.3.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scipy>=1.9.2,<2.0.0',
 'shapely>=1.8.5.post1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

extras_require = \
{'all': ['geojson>=2.5.0,<3.0.0',
         'esda>=2.4.3,<3.0.0',
         'geomstats>=2.5.0,<3.0.0']}

setup_kwargs = {
    'name': 'cellseg-gsontools',
    'version': '0.1.0.1',
    'description': 'Toolbelt for merging and extracting features from geojson masks.',
    'long_description': '**Spatial analysis tools for WSI segmentation maps.**\n',
    'author': 'Okunator',
    'author_email': 'oskari.lehtonen@helsinki.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/okunator/cellseg_gsontools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
