try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Indeed Data Mining Project',
    'author': 'cappetta',
    'url': 'https://github.com/cappetta/indeedSearch',
    'download_url': 'https://github.com/cappetta/indeedSearch',
    'author_email': 'thomas.cappetta@gmail.com',
    'version': '1.',
    'install_requires': ['PyYAML',],
    'packages': ['indeedSearch'],
    'scripts': [],
    'name': 'indeedSearch'
}

setup(**config)
