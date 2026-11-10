@echo off
title SiteBlitz Lead Intelligence OS
rem Run from the folder this file lives in, so a double-click from Explorer works too.
cd /d "%~dp0"
echo ================================================================
echo   SiteBlitz Lead Intelligence OS — Starting Full Stack
echo ================================================================
echo Starting Backend (FastAPI :8000) and Frontend (Vite :5173)...
echo.
rem The project's virtual environment is .venv (README); venv is the older name.
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" run_all.py
) else if exist "venv\Scripts\python.exe" (
  "venv\Scripts\python.exe" run_all.py
) else (
  echo No virtual environment found. Create one first: python -m venv .venv
  echo then: .venv\Scripts\python.exe -m pip install -e ".[dev]"
)
pause
