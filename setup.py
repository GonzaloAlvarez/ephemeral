#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import shutil, os
from distutils.command.clean import clean as Clean
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

class CleanCommand(Clean):
    description = "Remove build directories, and compiled file in the source tree"

    def run(self):
        Clean.run(self)
        if os.path.exists('build'):
            shutil.rmtree('build')
        cwd = os.path.abspath(os.path.dirname(__file__))
        for dirpath, dirnames, filenames in os.walk(cwd):
            for filename in filenames:
                if (filename.endswith('.so') or filename.endswith('.pyd')
                             or filename.endswith('.dll')
                             or filename.endswith('.pyc')
                             or filename.startswith('.DS_Store')
                             or filename.startswith('.coverage')):
                    os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if (dirname == '__pycache__' or dirname == '.pytest_cache'
                            or dirname == '.eggs'
                            or dirname.endswith('.egg-info')):
                    shutil.rmtree(os.path.join(dirpath, dirname))

        if self.all:
            if os.path.exists('.venv'):
                shutil.rmtree('.venv')


setup(
    author="Gonzalo Alvarez",
    author_email='gonzaloab@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    cmdclass={'clean': CleanCommand},
    description="Ephemeral Devtools Toolkit",
    entry_points={
        'console_scripts': [
            'eph=eph:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ephemeral, eph, devtools, toolkit',
    name='ephemeral',
    packages=find_packages(include=['ephemeral']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/GonzaloAlvarez/ephemeral',
    version='0.1.0',
    zip_safe=False,
)
