# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biochatter']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.146,<0.0.147',
 'nltk>=3.8.1,<4.0.0',
 'openai>=0.27.8,<0.28.0',
 'pymilvus==2.2.8',
 'pymupdf>=1.22.3,<2.0.0',
 'redis>=4.5.5,<5.0.0',
 'retry>=0.9.2,<0.10.0',
 'tiktoken>=0.4.0,<0.5.0']

extras_require = \
{'streamlit': ['streamlit>=1.23.1,<2.0.0']}

setup_kwargs = {
    'name': 'biochatter',
    'version': '0.1.2',
    'description': 'Backend library for conversational AI in biomedicine',
    'long_description': '# biochatter\nThis repository contains the `biochatter` Python package, a generic backend library for the connection of biomedical applications to conversational AI. Used in [ChatGSE](https://chat.biocypher.org), which is being developed at https://github.com/biocypher/ChatGSE. More to come, so stay tuned!\n\n## Installation\nTo use the package, install it from PyPI, for instance using pip (`pip install biochatter`) or Poetry (`poetry add biochatter`).\n',
    'author': 'Sebastian Lobentanzer',
    'author_email': 'sebastian.lobentanzer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
