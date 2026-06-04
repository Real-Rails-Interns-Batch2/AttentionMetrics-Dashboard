import json
import os
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="POC-45 Revenue Simulator API")

# CORS ക്രമീകരണം
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://attention-metrics-web.onrender.com"], # നിങ്ങളുടെ ഫ്രണ്ട്‌എൻഡ് URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Data from data.json
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {"platforms": data, "verticals": []}
    except Exception as e:
        logger.error(f"Error loading JSON: {e}")
    # ഫയൽ ഇല്ലെങ്കിൽ ഡിഫോൾട്ട് ഡാറ്റ
    return {
        "platforms": [
            {"id": "1", "name": "YouTube", "icon": "📺", "category": "Video", "dau": 100, "session": 40, "adLoad": 5, "cpm": 15.0, "creatorSplit": 55, "color": "#ff0000"},
            {"id": "2", "name": "TikTok", "icon": "🎵", "category": "Short-form", "dau": 150, "session": 30, "adLoad": 8, "cpm": 10.0, "creatorSplit": 40, "color": "#00f2ea"}
        ],
        "verticals": [
            {"label": "Gaming", "value": 12}, {"label": "Education", "value": 8}, {"label": "Tech", "value": 20}
        ]
    }

data = load_data()
PLATFORMS_DATA = data.get("platforms", [])
VERTICAL_CPMS_DATA = data.get("verticals", [])

# Models
class Platform(BaseModel):
    id: str
    name: str
    icon: str
    category: str
    dau: int
    session: int
    adLoad: int
    cpm: float
    creatorSplit: int
    color: str

class VerticalCPM(BaseModel):
    label: str
    value: float # float ആക്കി മാറ്റി (ചിലപ്പോൾ വാല്യൂ ഡെസിമൽ ആകാൻ സാധ്യതയുണ്ട്)

# Routes
@app.get("/")
async def root():
    return {"message": "API is running successfully!"}

@app.get("/api/platforms", response_model=List[Platform])
async def get_platforms():
    return PLATFORMS_DATA

@app.get("/api/cpm-verticals", response_model=List[VerticalCPM])
async def get_cpm_verticals():
    return VERTICAL_CPMS_DATA

@app.get("/api/platforms/{platform_id}", response_model=Platform)
async def get_platform(platform_id: str):
    platform = next((p for p in PLATFORMS_DATA if p["id"] == platform_id), None)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return platform

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
