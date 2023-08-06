# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geom_render']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1.2', 'numpy>=1.17', 'tqdm>=4.41.1', 'wf-cv-utils>=0.3.1']

setup_kwargs = {
    'name': 'wf-geom-render',
    'version': '0.5.0',
    'description': 'A library for projecting 3D geoms into 2D videos',
    'long_description': '# geom_render\n\nA library for projecting 3D geoms onto 2D videos\n',
    'author': 'Theodore Quinn',
    'author_email': 'ted.quinn@wildflowerschools.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WildflowerSchools/wf-geom-render',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
