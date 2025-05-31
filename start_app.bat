@echo off
echo Starting AI Sports Betting Platform...
echo.
echo Starting Backend (FastAPI)...
start cmd /k "cd backend && python -m uvicorn app.main:app --reload --port 8000"
echo Waiting for backend to start...
timeout /t 8 /nobreak > nul
echo Starting Frontend (Vite)...
start cmd /k "cd frontend && npm run dev"
echo.
echo Platform is starting up!
echo Backend: http://localhost:8000/docs (FastAPI docs)
echo Frontend: http://localhost:3000
echo If you see errors, check logs in the logs/ folder.
echo To stop, close both terminals or use Ctrl+C in each.
pause
