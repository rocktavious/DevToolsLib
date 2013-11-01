import os
import sys
import traceback

from DTL.api import apiUtils, Path

def main():
    local_path = Path(sys.argv[0]).parent
    support_files_dir = local_path.join('DTL_support', 'PythonDev')
    
    dev_path = Path(raw_input('Enter path to create the development environment at:'))
    environment_path = dev_path.join('PythonDev')
    if not dev_path.exists() :
        if raw_input('Path does not exist, create it? y/n:') == 'y' :
            dev_path.makedirs()
        else:
            raise Exception('Invalid Location')
        
    if environment_path.exists():
        if raw_input('Development environment already exists, delete it? y/n:') == 'y' :
            environment_path.rmtree()
        else:
            raise Exception('Development path already exists!')
    
    support_files_dir.copytree(environment_path)
    local_path.copytree(environment_path.join('3rdparty','DevToolsLib'))
    local_path.copytree(environment_path.join('Projects','DevToolsLib'))
    
    sys.path.append(environment_path.join('Environments'))
    import SetEnvironment
    SetEnvironment.main(environment_path.join('Environments','SetEnvironment.py'))
    
    
    
if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
        raw_input("Failed!")