@echo off 
start /B dev_appserver.py --port 1234 %DTL_TOOLS_PATH%
timeout /t 5 /nobreak > NUL
if exist chrome goto: CHROME
if exist firefox goto: FIREFOX
if exist iexplore goto: IE

:CHROME
start chrome localhost:1234
goto END
:FIREFOX
start firefox localhost:1234
goto END
:IE
start iexplore localhost:1234
goto END

:END
