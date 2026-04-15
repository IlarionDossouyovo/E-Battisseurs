@echo off
echo E-Battisseurs Setup for Windows
echo ==============================

echo Installing Python dependencies...
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To start the API:
echo   .venv\Scripts\python -m uvicorn main:app --reload
echo.
echo Or with Docker:
echo   docker-compose up -d