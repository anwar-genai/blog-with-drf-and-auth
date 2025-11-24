@echo off
echo ========================================
echo   Full-Stack Blog Platform
echo ========================================
echo.

REM Check if .env.local exists, create if not
if not exist "%~dp0frontend\.env.local" (
    echo Creating frontend\.env.local...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > "%~dp0frontend\.env.local"
    echo ✓ Created .env.local
    echo.
)

echo Starting Django Backend (Port 8000)...
start "Django Backend" cmd /k "cd /d %~dp0 && echo Django Backend Starting... && uv run daphne -b 127.0.0.1 -p 8000 config.asgi:application"

timeout /t 3

echo Starting Next.js Frontend (Port 3000)...
start "Next.js Frontend" cmd /k "cd /d %~dp0\frontend && echo Next.js Frontend Starting... && npm run dev"

echo.
echo ========================================
echo   Both Servers Starting...
echo ========================================
echo.
echo ► Django Backend:  http://localhost:8000
echo ► Next.js Frontend: http://localhost:3000
echo ► Login Page:      http://localhost:3000/login
echo.
echo Press any key to close this window...
pause > nul
