import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command
setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='craid',
    url='https://github.com/HausReport/ClubRaiders',
    author='Erlaed',
    author_email='Erlaed2@fdev.not',
    # Needed to actually package something
    #packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    packages=['craid','craid.eddb','craid.regions'],
    # Needed for dependencies
    #install_requires=['numpy'],
    # *strongly* suggested for sharing
    version='0.37',
    # The license can be anything you like
    license='MIT',
    description='Placeholder description',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
