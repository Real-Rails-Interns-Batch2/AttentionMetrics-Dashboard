import json
import os
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Attention Metrics API")

# CORS ക്രമീകരണം
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://attention-metrics-web.onrender.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# JSON ഡാറ്റയ്ക്ക് അനുസരിച്ചുള്ള മോഡൽ
class Platform(BaseModel):
    id: int
    user: str
    status: str
    is_synthetic: bool

# Load Data from data.json
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON: {e}")
    # ഫയൽ ഇല്ലെങ്കിൽ ഡിഫോൾട്ട് ഡാറ്റ
    return [
        {"id": 1, "user": "Jaliha Sherin", "status": "active", "is_synthetic": True},
        {"id": 2, "user": "Error User", "status": "invalid_input", "is_synthetic": True}
    ]

# ഡാറ്റ ലോഡ് ചെയ്യുന്നു
PLATFORMS_DATA = load_data()

# Routes
@app.get("/")
async def root():
    return {"message": "API is running successfully!"}

@app.get("/api/platforms", response_model=List[Platform])
async def get_platforms():
    return PLATFORMS_DATA

@app.get("/api/platforms/{platform_id}", response_model=Platform)
async def get_platform(platform_id: int):
    platform = next((p for p in PLATFORMS_DATA if p["id"] == platform_id), None)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return platform

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
