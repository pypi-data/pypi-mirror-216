# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miniscope_io']

package_data = \
{'': ['*']}

install_requires = \
['ipywidgets>=8.0.6,<9.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.25.0,<2.0.0',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'parse>=1.19.1,<2.0.0',
 'pydantic>=1.10.9,<2.0.0',
 'rich>=13.4.2,<14.0.0']

setup_kwargs = {
    'name': 'miniscope-io',
    'version': '0.1.0',
    'description': '',
    'long_description': '# miniscope-io\n\n(Demonstration project for a lab workshop on making modular, testable python code.\nFunctionality not guaranteed\n-<3 jonny)\n\n',
    'author': 'sneakers-the-rat',
    'author_email': 'JLSaunders987@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
