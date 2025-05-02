#!/user/bin/env python

import os

from setuptools import setup, find_packages


setup(
    name='brwyatt_web',
    version='0.1.0',
    author='Bryan Wyatt',
    author_email='brwyatt@gmail.com',
    description=('Web code for brwyatt.net'),
    license='GPLv3',
    keywords='aws web website serverless lambda',
    url='https://github.com/brwyatt/brwyatt.net',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=False,
    entry_points={},
    install_requires=[
        'boto3==1.7.4',
        'botocore==1.10.74',
        'Jinja2==3.1.3',
        'PyYAML==5.4',
    ]
)
