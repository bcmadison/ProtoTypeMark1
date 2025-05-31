@echo off
cd C:\Users\bcmad\OneDrive\Desktop\ProtoTypeMark1\backend
start cmd /k python server.py
timeout 5
cd C:\Users\bcmad\OneDrive\Desktop\ProtoTypeMark1\frontend
start cmd /k npm run dev
pause