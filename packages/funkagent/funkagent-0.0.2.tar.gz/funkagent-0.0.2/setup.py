# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['funkagent']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.8,<0.28.0']

setup_kwargs = {
    'name': 'funkagent',
    'version': '0.0.2',
    'description': 'Minimal agent framework using OpenAI functions',
    'long_description': '# FunkAgent\n\nGet started with:\n\n```\npip install funkagent\n```\n',
    'author': 'James Briggs',
    'author_email': 'james@aurelio.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
