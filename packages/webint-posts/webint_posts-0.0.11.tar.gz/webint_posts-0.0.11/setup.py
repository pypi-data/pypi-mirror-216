# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_posts', 'webint_posts.templates']

package_data = \
{'': ['*']}

install_requires = \
['micropub>=0.0', 'webint>=0.0']

entry_points = \
{'webapps': ['posts = webint_posts:app']}

setup_kwargs = {
    'name': 'webint-posts',
    'version': '0.0.11',
    'description': 'manage posts on your website',
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
