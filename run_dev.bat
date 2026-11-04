@echo off
title DropShip Full-Stack Dev Server Launcher
echo ========================================================
echo   Starting DropShip Full-Stack Development Platform
echo ========================================================
echo.

echo [1/2] Starting Django API Backend on http://127.0.0.1:8000 ...
start "DropShip Backend (Django)" cmd /k "cd /d %~dp0backend && ..\venv\Scripts\activate && python manage.py runserver 127.0.0.1:8000"

echo [2/2] Starting Nuxt 4 Frontend on http://localhost:3000 ...
start "DropShip Frontend (Nuxt)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================================
echo   Both servers have been launched in separate windows!
echo   - Storefront & Admin: http://localhost:3000
echo   - Django REST API:    http://127.0.0.1:8000/api/
echo   - Django Admin:       http://127.0.0.1:8000/admin/
echo ========================================================
pause
