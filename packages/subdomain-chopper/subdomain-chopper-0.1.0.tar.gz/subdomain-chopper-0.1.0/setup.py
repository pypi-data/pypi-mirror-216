# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['subdomain_chopper']
setup_kwargs = {
    'name': 'subdomain-chopper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Henry Post',
    'author_email': 'henryfbp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
