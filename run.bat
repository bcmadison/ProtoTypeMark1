@echo off
cd backend
echo Starting backend...
start cmd /k python server.py
cd ..
timeout /t 5
cd frontend
echo Starting frontend...
start cmd /k npm run dev
cd ..
echo.
echo App is running!
echo Logs will be saved automatically when you close it.
pause
