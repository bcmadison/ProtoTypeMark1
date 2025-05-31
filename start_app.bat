@echo off
echo Starting AI Sports Betting Platform...
echo.
echo Starting Backend...
start cmd /k "cd backend && python server.py"
timeout /t 5 /nobreak > nul
echo Starting Frontend...
start cmd /k "cd frontend && npm start"
echo.
echo Platform is starting up!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
pause
