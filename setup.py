#!/usr/bin/env python

import os.path
from distutils.core import setup

package_name = 'prex'
package_version = '0.0.1'

# doc_dir = os.path.join('share', 'doc', package_name)

# data_files = ['LICENSE', 'README.md']

setup(name=package_name,
    version=package_version,
    description='Search and replace in files with regular expressions',
    author='Malthe Jørgensen',
    author_email='malthe.jorgensen@gmail.com',
    url='https://github.com/malthejorgensen/prex',
    py_modules=['prex'],
    # install_requires=[],
    # data_files=[
    #     (doc_dir, data_files),
    # ],
    entry_points={
        'console_scripts': [
            'prex = prex:cmdline_entry_point',
        ],
    },
    license="BSD 2-Clause",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing',
    ],
)
