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
import re

# Create the app
app = FastAPI(
    title="TEXT ANALYSIS API",
    description="Analyze text and get detailed statistics",
    version="1.0.0"
)

# DATA MODELS
class TextInput(BaseModel):
    text: str

    class Config:
        example = {
            "text": "Hey i am eric, i am building this cool project"
        }

class TextAnalysisResponse(BaseModel):
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
    result: float
    unit: str

# HELPER FUNCTIONS
def clean_text(text: str) -> str:
    # Remove special character but keep spaces and punctudation for analysis
    return text.strip()

def count_words(text: str) -> int:
    # divide the string into list of substrings
    words = text.split()

    return len(words)

def count_characters(text: str) -> tuple:
    char_with_spaces = len(text)
    char_without_spaces = len(text.replace(" ", ""))
    return char_with_spaces, char_without_spaces

def count_sentences(text: str) -> int:
    # Cut the text into multiple pieces upon finding .!?
    # + ensures ... !!! ??? are treated as single breaks
    sentences = re.split(r'[.!?]+', text)

    # Filter out empty strings
    sentences = [s.strip() for s in sentences if s.strip()]

    # count the pieces & ensure result is atleast 1 sentence
    return max(1, len(sentences))

def get_words_list(text: str) -> List[str]:
    text = text.lower()

    # Remove punctuations but keep spaces
    text = re.sub(r'[^\w\s]', '',  text)

    # Split into words
    words = text.split()

    return words

def calculate_average_word_length(words: List[str]) -> float:
    # Validation check
    if not words:
        return 0

    total_length = sum(len(word) for word in words)
    average_length = total_length / len(words)

    return round(average_length, 2)

def calculate_average_sentence_length(text: str, sentence_count: int) -> float:
    # Calculate average words per sentence
    words = text.split()

    # Validation check
    if sentence_count == 0:
        return 0

    average_sentence_length = len(words) / sentence_count

    return round(average_sentence_length, 2))