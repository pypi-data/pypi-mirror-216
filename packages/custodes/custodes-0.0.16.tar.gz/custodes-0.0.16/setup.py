# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['custodes']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=9.0.5,<10.0.0',
 'aiohttp>=3.8.4,<4.0.0',
 'codefast>=23.4.18.13,<24.0.0.0',
 'rich>=13.3.5,<14.0.0',
 'simauth==0.0.9',
 'urllib3==1.26.15']

setup_kwargs = {
    'name': 'custodes',
    'version': '0.0.16',
    'description': '',
    'long_description': "\nApp guardians.\n\n# Usage\n```python\nimport asyncio\nfrom typing import Any, Dict\n\nfrom codefast.asyncio.rabbitmq import consume\nfrom rich import print\n\nfrom custodes.server import get\nfrom custodes.client import post\n\nasync def main():\n    return await asyncio.gather(\n        post('custodes server', {'code': 0, 'message': 'OK'}, loop=True, expire=120),\n        get()\n    )\n\nif __name__ == '__main__':\n    cf.info('custodes server started...')\n    asyncio.run(main())\n\n```\n",
    'author': 'tompz',
    'author_email': 'tompz@tompz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
