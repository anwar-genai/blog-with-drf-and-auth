@echo off
echo Starting Django Backend...
echo.
cd /d "%~dp0"
uv run daphne -b 127.0.0.1 -p 8000 config.asgi:application
pause
