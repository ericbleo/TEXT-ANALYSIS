"""
    TEXT ANALYSIS API
    FastAPI app that analyzes text & returns detailed statistics

    RUN COMMAND: uvicorn main:app --reload
    Visit "http://localhost:8000/docs" for interactive documentation
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Tuple
import math

# Create the app
app = FastAPI(
    title="TEXT ANALYSIS API",
    description="Analyze text and get detailed statistics",
    version="1.0.0"
)

# DATA MODELS
class TextInput(BaseModel):
    """Input model for text analysis"""
    text: str

    class Config:
        example = {
            "text": "Hey i am eric, i am building this cool project"
        }

    class TextAnalysisResponse(BaseModel):
        """Response model with all text statistics"""
        word_count: int
        character_count: int
        sentence_count: int
        average_word_length: float
        average_sentence_length: float
        most_common_words: List[Tuple[str, int]]
        unique_words: int
        reading_time_minutes: float
        sentiment: str
        sentiment_confidence: float
        readability_score: float
        language_stats: Dict

    class SimpleResponse(BaseModel):
        """Simple response model"""
        result: float
        unit: str