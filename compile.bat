rmdir /s /q %~dp0build
rmdir /s /q %~dp0DevToolsLib.egg-info
rmdir /s /q %~dp0dist

python setup.py bdist_wininst
python setup.py bdist_egg

rmdir /s /q %~dp0build
rmdir /s /q %~dp0DevToolsLib.egg-info


pause