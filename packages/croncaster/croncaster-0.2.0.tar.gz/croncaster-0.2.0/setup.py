# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['croncaster']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'pyyaml>=6.0,<7.0', 'yamt>=0.1.3.1,<0.2.0.0']

setup_kwargs = {
    'name': 'croncaster',
    'version': '0.2.0',
    'description': 'cached shell command caster based on rotating state machine',
    'long_description': '# croncaster\n[![PyPI version](https://badge.fury.io/py/croncaster.svg)](https://badge.fury.io/py/croncaster)\n![PyPI downloads per mounth](https://img.shields.io/pypi/dm/croncaster)\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/lightmanLP/croncaster)\n\nSimple tool for periodic events based on timeout. Cron is supposed to be used as runtime base.\n\n## How to use\nJust add cron that runs croncaster every `n`.\n```crontab\n@hourly python3 -m croncaster\n```\nThen use `n` as one step in config. Pretty simple.\n',
    'author': 'lightmanLP',
    'author_email': 'liteman1000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
