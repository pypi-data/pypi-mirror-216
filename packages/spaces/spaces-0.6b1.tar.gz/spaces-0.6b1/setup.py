# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spaces', 'spaces.gpu']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.9.5,<6.0.0',
 'pydantic>=1.10.8,<2.0.0',
 'requests>=2.29.0,<3.0.0',
 'typing-extensions>=4.5.0,<5.0.0']

setup_kwargs = {
    'name': 'spaces',
    'version': '0.6b1',
    'description': 'Utilities for Hugging Face Spaces',
    'long_description': '# Hugging Face Spaces\n\n## Installation\n\n`pip install spaces`\n',
    'author': 'Charles Bensimon',
    'author_email': 'charles@huggingface.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://huggingface.co',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
