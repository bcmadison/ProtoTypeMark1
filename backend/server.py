from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

from routes.settings import router as settings_router
from routes.analytics_route import router as analytics_router
from routes.predictions import router as predictions_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(settings_router)
app.include_router(analytics_router)
app.include_router(predictions_router, prefix="/api/predictions")

logger = logging.getLogger(__name__)

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Predictions endpoint (no prefix)
@app.get("/predictions")
def get_predictions():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "predictions_latest.csv")
    if not os.path.exists(csv_path):
        return []
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")

# Lineup endpoint
@app.get("/api/lineup")
async def get_lineup():
    # TODO: integrate real optimization logic
    sample = {"sport": "nba", "lineup": ["Player A", "Player B", "Player C"]}
    return {"status": "success", "data": sample}

# Analytics endpoint
@app.get("/api/analytics")
async def get_analytics():
    # TODO: compute ROI and performance trends
    trends = {"ROI": [5.2, 6.1, 4.8], "dates": ["2025-05-27", "2025-05-28", "2025-05-29"]}
    return {"status": "success", "trends": trends}

# SHAP explainability endpoint
@app.get("/api/shap")
async def get_shap():
    # TODO: integrate SHAP values generation
    return {"status": "success", "values": []}

# Settings endpoint
@app.get("/api/settings")
async def get_settings():
    # Return UI + strategy config
    settings = {"sports": ["All Sports", "NBA", "MLB", "NHL", "Soccer"], "confidenceLevels": [50, 60, 70, 80, 90]}
    return {"status": "success", "settings": settings}

# Feedback endpoint
@app.post("/api/feedback")
async def post_feedback(request: dict):
    # TODO: capture and store user feedback
    return {"status": "success", "received": request}

# WebSocket for live scores (example)
@app.websocket("/ws/scores")
async def websocket_scores(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        logger.info("Client disconnected")
