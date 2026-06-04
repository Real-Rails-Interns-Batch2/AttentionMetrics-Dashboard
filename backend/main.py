import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/api/platforms", response_model=List[Platform])
def get_platforms():
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(file_path, 'r') as f:
        return json.load(f)
