@echo off
setlocal enabledelayedexpansion

REM set "port=80"
REM for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%port%"') do (
REM     set "pid=%%a"
REM     taskkill /F /PID !pid! >nul 2>&1
REM )
REM echo All programs on port %port% have been terminated.

REM set "port=8080"
REM for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%port%"') do (
REM     set "pid=%%a"
REM     taskkill /F /PID !pid! >nul 2>&1
REM )
REM echo All programs on port %port% have been terminated.

taskkill /F /IM python.exe /T

echo Starting backend
set "PYTHONPATH=friendhub/backend/src;."
set "PROFILE=yes;."
start "" /B py friendhub/backend/src/main.py

REM echo Starting frontend
REM cd ..\FriendHub-frontend
REM start "" /B trunk serve --features for_web
REM start "" "http://127.0.0.1:8080"

endlocal
