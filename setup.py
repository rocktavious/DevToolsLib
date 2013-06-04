import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

import DTL

setup( 
    name='DevToolsLib',
    version=DTL.__version__,
    author='Kyle Rockman',
    author_email='kyle.rockman@.com',
    packages = find_packages(),
    package_data = {
        # If any subfolder contains these extensions, include them:
        '': ['*.txt', '*.rst','*.stylesheet','*.ui','*views/*.ui']
        },
    zip_safe=True,
    url='https://github.com/rocktavious/DevToolsLib',
    license='LICENSE.txt',
    description='Multiplatform, multiapplication tools development api',
    long_description=open('README.txt').read(),
)