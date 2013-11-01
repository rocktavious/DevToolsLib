import os
import sys

python_packages = os.environ.get('PYTHON_PACKAGES')
if python_packages :
    for dir in os.listdir(python_packages):
        sys.path.insert(0, os.path.join(python_packages, dir))

python_env = os.environ.get('PYTHON_ENVIRONMENT')
if python_env :
	sys.path.insert(0, python_env)
