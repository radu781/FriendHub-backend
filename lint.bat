@echo off
setlocal enabledelayedexpansion

set "PYTHONPATH=friendhub/backend/src;."
start "" /B ruff .
