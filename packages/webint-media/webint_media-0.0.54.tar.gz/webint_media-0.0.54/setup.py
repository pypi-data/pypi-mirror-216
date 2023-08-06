# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_media', 'webint_media.templates']

package_data = \
{'': ['*']}

install_requires = \
['webint>=0.0', 'yt-dlp>=2023.3.4,<2024.0.0']

entry_points = \
{'webapps': ['media = webint_media:app']}

setup_kwargs = {
    'name': 'webint-media',
    'version': '0.0.54',
    'description': 'manage media on your website',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
