rmdir /s /q %~dp0build
rmdir /s /q %~dp0DevTools.egg-info
rmdir /s /q %~dp0dist

setup.py bdist_wininst
setup.py bdist_rpm

pause