# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['banditcoot', 'banditcoot.algorithms', 'banditcoot.arms', 'banditcoot.utility']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'banditcoot',
    'version': '0.1.6',
    'description': 'Python module for developing and testing multi-armed bandits',
    'long_description': 'Banditcoot\n====================\n\n<img align="left" width="75" src="https://github.com/dan-kwon/banditcoot/blob/master/resources/Banditcoot.png"/> \n\n**banditcoot** is a Python module is intended for my own personal use when developing and testing multi-armed bandit algorithms. Forked from the accompanying [code repository](https://github.com/johnmyleswhite/BanditsBook) for [Bandit Algorithms for Website Optimization](https://www.oreilly.com/library/view/bandit-algorithms-for/9781449341565/).\n\n*Any use of this code is at your own risk.*\n</br>\n\n## Installation\n--------------------\nRecommended method of installation is to use pip \n```\npip install banditcoot\n```\n\n\n## Quickstart\n--------------------\n',
    'author': 'dan-kwon',
    'author_email': 'danielkwon02@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
