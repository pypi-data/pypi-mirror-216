#!/usr/bin/env python
from setuptools import setup, find_packages
from blog import __version__

setup(
    name='danemco-blog',
    version=__version__,
    description="A fine blog app",
    author="Danemco, LLC",
    author_email='dev@velocitywebworks.com',
    url='https://gitlab.com/virgodev/lib/danemco-blog',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=2.0',
        'Pillow',
        'pytz',
    ],
)
