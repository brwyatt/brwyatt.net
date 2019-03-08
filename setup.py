#!/user/bin/env python

import os

from setuptools import setup, find_packages


def package_files(package, directory):
    package_path = os.path.join('src', package)
    paths = []
    for (path, directories, filenames) in os.walk(os.path.join(package_path,
                                                               directory)):
        for filename in filenames:
            paths.append(os.path.relpath(os.path.join(path, filename),
                                         package_path))
    return paths

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
    include_package_data=True,
    package_data={
        'brwyatt_web': package_files('brwyatt_web', 'pages/templates')
    },
    entry_points={},
    install_requires=[
        'boto3',
        'botocore',
        'Jinja2',
    ]
)
