from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
import json
import time

app = FastAPI(title="RailIntel Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mocked Data Base State
db = {
    "forecast": [
        {"time": "14:00", "projected_delay_risk": 2},
        {"time": "15:00", "projected_delay_risk": 5},
        {"time": "16:00", "projected_delay_risk": 12},
        {"time": "17:00", "projected_delay_risk": 18},
        {"time": "18:00", "projected_delay_risk": 45},
    ],
    "alerts": [
        {"ID": "INC-A1", "Severity": "CRITICAL", "Type": "Track Blockage", "Response": "DISPATCHED"},
        {"ID": "INC-B2", "Severity": "HIGH", "Type": "Signal Comms Failure", "Response": "PENDING"},
    ],
    "commands": []
}

class CommandRequest(BaseModel):
    operator_id: str
    command_type: str
    target: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "RailIntel Operation Backend Active"}

@app.get("/forecast")
def get_forecast():
    return {"status": "success", "data": db["forecast"]}

@app.get("/alerts")
def get_alerts():
    return {"status": "success", "data": db["alerts"]}

@app.post("/execute-command")
def execute_command(req: CommandRequest):
    if not req.operator_id or not req.command_type:
        raise HTTPException(status_code=400, detail="Invalid Command Structure")
    
    log_entry = {
        "timestamp": time.time(),
        "operator_id": req.operator_id,
        "command_type": req.command_type,
        "target": req.target,
        "status": "SUCCESS"
    }
    db["commands"].append(log_entry)
    
    return {"status": "success", "message": "COMMAND EXECUTED", "log": log_entry}

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(1)
            await websocket.send_json({"train": "TRN-801", "status": "CRITICAL", "speed": 160, "latency": "14ms"})
    except Exception as e:
        print(f"WebSocket Client Disconnected: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
