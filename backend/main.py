import json
import os
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Attention Metrics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://attention-metrics-web.onrender.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Platform(BaseModel):
    id: int
    user: str
    status: str
    is_synthetic: bool
    dau: Optional[int] = 0
    session: Optional[int] = 0
    adLoad: Optional[int] = 0
    cpm: Optional[float] = 0.0
    creatorSplit: Optional[int] = 0
    color: Optional[str] = "#000000"

def load_data():
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        return []

PLATFORMS_DATA = load_data()

@app.get("/api/platforms", response_model=List[Platform])
async def get_platforms():
    return PLATFORMS_DATA

@app.get("/")
async def root():
    return {"message": "API is running!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
