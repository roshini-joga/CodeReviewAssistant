from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Code Review Assistant",
    description="An intelligent code review system using LLMs",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class CodeReviewRequest(BaseModel):
    code: str
    language: str
    context: Optional[str] = None

class CodeReviewResponse(BaseModel):
    suggestions: List[str]
    quality_score: float
    potential_bugs: List[str]
    improvement_areas: List[str]

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to AI Code Review Assistant API"}

@app.post("/api/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    try:
        # TODO: Implement code review logic using LLM
        # This is a placeholder response
        return CodeReviewResponse(
            suggestions=["Consider adding type hints", "Add docstring to function"],
            quality_score=0.85,
            potential_bugs=["Possible null reference in line 15"],
            improvement_areas=["Code organization", "Error handling"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 