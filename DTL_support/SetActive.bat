@echo off
Setlocal EnableDelayedExpansion
SETX JENKINS_URL "http://jenkins.ciaus.local/"
SETX PYTHON_ENVIRONMENT %~dp0
SETX PYTHON_PACKAGES %~dp0..\..\3rdparty
echo."%PATH%"|findstr /C:"Python27" >nul 2>&1
if errorlevel 1 (
   echo Adding python27 to path
   set NEW_PATH=%NEW_PATH%;C:\Python27
)
echo."%PATH%"|findstr /C:"%PYTHON_ENVIRONMENT%Tools" >nul 2>&1
if errorlevel 1 (
   echo Adding python environment tools to path
   set NEW_PATH=%NEW_PATH%;%PYTHON_ENVIRONMENT%Tools
)
if "%NEW_PATH%" NEQ "" (
   SETX /m Path "%Path%%NEW_PATH%"
)
set py_loc=C:\Python27\Lib\site-packages\
set py_env_pth=%py_loc%environment.pth
if exist %py_env_pth% (
	del %py_env_pth%
)
set py_env_py=%py_loc%environment.py
if exist %py_env_py% (
	del %py_env_py%
)
if exist %py_loc% (
	mklink %py_env_pth% %~dp0environment.pth
	mklink %py_env_py% %~dp0environment.py
)

set maya_loc=%UserProfile%\Documents\maya\scripts\
echo %maya_loc%
set maya_env_pth=%maya_loc%environment.pth
if exist %maya_env_pth% (
	del %maya_env_pth%
)
set maya_env_py=%maya_loc%environment.py
if exist %maya_env_py% (
	del %maya_env_py%
)
set maya_user_setup=%maya_loc%userSetup.py
if exist %maya_user_setup% (
	del %maya_user_setup%
)
if exist %maya_loc% (
	call mklink %maya_env_pth% %~dp0environment.pth
	call mklink %maya_env_py% %~dp0environment.py
	call mklink %maya_user_setup% %~dp0userSetup.py
)
