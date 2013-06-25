from setuptools import setup, find_packages

import DTL

setup( 
    name='DTL',
    version=DTL.__version__,
    author='Kyle Rockman',
    author_email='kyle.rockman@mac.com',
	install_requires=['requests==1.2.3'],
    packages = find_packages(),
    package_data = {
        # If any subfolder contains these extensions, include them:
        '': ['*.txt', '*.rst','*.stylesheet','*.ui','*views/*.ui'],
        },
    zip_safe=False,
    url='https://github.com/rocktavious/DevToolsLib',
    license=open('LICENSE.txt').read(),
    description='Multiplatform tools development api',
    long_description=open('README.txt').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing',
    ],
)