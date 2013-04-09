import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup( 
    name='DevTools',
    version=open('VERSION.txt').read(),
    author='Kyle Rockman',
    author_email='kyle.rockman@.com',
    packages = find_packages(),
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst','*.stylesheet','*.ui','*views/*.ui']
        },
    url='',
    license='LICENSE.txt',
    description='Multiplatform, multiapplication tools development api',
    long_description=open('README.txt').read(),
)