rmdir /s /q %~dp0build
rmdir /s /q %~dp0DTL.egg-info
rmdir /s /q %~dp0dist

python setup.py register sdist bdist_egg bdist_wininst upload

rmdir /s /q %~dp0build
rmdir /s /q %~dp0DTL.egg-info


pause