# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['honkaistarrail', 'honkaistarrail.src.data.gacha']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'honkaistarrail',
    'version': '0.0.5',
    'description': 'Asynchronous module for working with API Honkai: Star Rail',
    'long_description': '<p align="center">\n  <img src="https://raw.githubusercontent.com/DEViantUA/HonkaiStarRail.py/main/Readme/HSR-BANNER.png" />\n</p>\n\n# Asynchronous module for working with API Honkai: Star Rail\n\nAt the moment it only supports counting guarantors and getting a jumps \n\n### Installation: \n```\npip install honkaistarrail\n```\nPyPi: [OPEN](https://pypi.org/project/honkaistarrail/)\n\nYou can also see other usage examples here: [OPEN](https://github.com/DEViantUA/starrail.py/tree/main/Examples)\n\nInstructions for getting a link to the history of jumps: [OPEN](https://github.com/DEViantUA/starrail.py/blob/main/Instruction.md)\n\n### ID Banned:\n``1`` - Event Banner\n``2`` - Light Cone\n``3`` - Standart Banner\n\n\n### Launc:\n\n```py\n# Copyright 2023 DEViantUa <t.me/deviant_ua>\n# All rights reserved.\n\n\'\'\'\nThis method returns the full history of jumps for the \nlast 3 months, does not return the results of jumps \nand how much is left before the guarantor.\n\'\'\'\n\nimport asyncio\nfrom honkaistarrail import starrail\n\nasync def get_jump_history():\n    link = ""\n    async with starrail.Jump(link = link,banner = 1,lang = "en") as hist:\n        async for key in hist.get_history():\n            for info in key:\n                print(f\'[{info.type}] Name: {info.name} ({info.rank}*) - {info.time.strftime("%d.%m.%Y %H:%M:%S")}\')\n\n\nasyncio.run(get_jump_history())\n```\n\n\n# In developing:\n\n1. Automatic code redemption.\n2. Automatic collection of daily marks on HoYoLab.\n\n___\n<p align="center">\n  <img src="https://raw.githubusercontent.com/DEViantUA/HonkaiStarRail.py/main/Readme/%D0%91%D0%B5%D0%B7-%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8-1.png" />\n</p>\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DEViantUA/HonkaiStarRail.py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
