from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

from security_engine import PasswordIntelligenceEngine

app = FastAPI(title="Password Intelligence Platform API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Engine
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Check local 'datasets' folder (for Render) or parent 'datasets' (for local dev)
local_path = os.path.join(BASE_DIR, "datasets/common_passwords.txt")
parent_path = os.path.join(BASE_DIR, "../datasets/common_passwords.txt")
DATASET_PATH = local_path if os.path.exists(local_path) else parent_path

engine = PasswordIntelligenceEngine(dictionary_path=DATASET_PATH)

class PasswordRequest(BaseModel):
    password: str

class AnalysisResponse(BaseModel):
    entropy: float
    findings: List[str]
    crack_time: dict
    score: int
    label: str
    color: str
    advice: List[str]

class GeneratorSettings(BaseModel):
    length: int = 16
    use_symbols: bool = True

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_password(req: PasswordRequest):
    p = req.password
    if not p:
        return AnalysisResponse(
            entropy=0, findings=[], crack_time={}, score=0, 
            label="N/A", color="#888", advice=["Enter a password to begin."]
        )
    
    entropy = engine.calculate_entropy(p)
    findings = engine.detect_patterns(p)
    crack_time = engine.estimate_crack_time(entropy)
    status = engine.get_score_and_label(entropy, findings)
    advice = engine.get_ai_advice(p, findings, entropy)
    
    return AnalysisResponse(
        entropy=entropy,
        findings=findings,
        crack_time=crack_time,
        score=status["score"],
        label=status["label"],
        color=status["color"],
        advice=advice
    )

@app.post("/generate")
async def generate_password(settings: GeneratorSettings):
    pwd = engine.generate_secure_password(settings.length, settings.use_symbols)
    # Also analyze the generated one
    entropy = engine.calculate_entropy(pwd)
    return {"password": pwd, "entropy": entropy}

@app.get("/health")
async def health():
    return {"status": "operational", "engine": "ready"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
