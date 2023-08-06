from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install
import os
import sys

VERSION = 'v205.0.0'

class PostInstallCommand(install):
     def run(self):
         install.run(self)
         print ("Hello daneee the system was crunched")
         

setup(
        name='crunchie',
        author='daneee',
        author_email='daneee@example.com',
        version=VERSION,
        packages=['crunchie'],
        include_package_data=True,
        license='MIT',
        description=('''Package that does absolutely nothing '''),
        cmdclass={
            'install': PostInstallCommand
        },
)