@echo off
setlocal

rem Read the values of PARAMETER1 and PARAMETER2 from the configuration file
for /f "tokens=2 delims==" %%a in ('findstr /b "ip=" adinat.conf') do set ip=%%a
for /f "tokens=2 delims==" %%a in ('findstr /b "port=" adinat.conf') do set port=%%a

rem Execute the command with ip and port as parameters
echo Running command with parameters: %ip% and %port%
python client.py %ip%:%port%

endlocal