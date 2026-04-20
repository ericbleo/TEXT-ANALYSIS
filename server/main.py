"""
    TEXT ANALYSIS API
    FastAPI app that analyzes text & returns detailed statistics

    RUN COMMAND: uvicorn main:app --reload
    Visit "http://localhost:8000/docs" for interactive documentation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Tuple
import re
from collections import Counter

# Create the app
app = FastAPI(
    title="TEXT ANALYSIS API",
    description="Analyze text and get detailed statistics",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    character_count_no_spaces: int
    sentence_count: int
    average_word_length: float
    average_sentence_length: float
    most_common_words: List[Tuple[str, int]]
    unique_words: int
    reading_time_minutes: float
    sentiment: str
    sentiment_confidence: float
    readability_score: float
    language_statistics: Dict

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

    return round(average_sentence_length, 2)

def get_most_common_words(words: List[str], n: int = 5) -> List[Tuple[str, int]]:
    # Validation check
    if not words:
        return []

    # Filter out words less than 3 characters
    filtered_words = [w for w in words if len(w) >=3]
    if not filtered_words:
        return []

    word_frequency = Counter(filtered_words)

    return word_frequency.most_common(n)

def count_unique_words(words: List[str]) -> int:
    # Set helps with ignoring duplicate values
    unique_words = set(word.lower() for word in words)

    return len(unique_words)

def calculate_reading_time(word_count: int, words_per_minute: int = 200) -> float:
    # Validation check
    if not word_count:
        return 0

    reading_time = word_count / words_per_minute
    return round(reading_time, 2)

def sentiment_analyser(text: str) -> tuple:
    text_lower = text.lower()

    # Positive words
    positive_words = [
        'good', 'great', 'excellent', 'amazing', 'awesome', 'love', 'perfect',
        'wonderful', 'fantastic', 'best', 'beautiful', 'happy', 'joy', 'brilliant',
        'superb', 'outstanding', 'exceptional', 'favorable', 'positive', 'pleasant',
        'delightful', 'satisfying', 'enjoyable', 'marvelous', 'impressive', 'splendid',
        'cheerful', 'pleasing', 'admirable', 'remarkable', 'cool', 'fabulous', 'charming',
        'graceful', 'friendly', 'nice', 'trustworthy', 'rewarding', 'fun', 'enthusiastic',
        'prosperous', 'radiant', 'relaxed', 'lovely', 'helpful', 'wise', 'supportive',
        'dynamic', 'inspiring', 'accomplished', 'blissful', 'euphoric', 'lively', 'thankful',
        'optimistic', 'progressive', 'energetic', 'motivated', 'memorable', 'genius', 'endearing',
        'outstanding', 'proud', 'magnificent', 'positivity', 'upbeat', 'glad', 'elated', 'ecstatic',
        'triumphant', 'appreciated', 'fortunate', 'gracious', 'cooperative', 'polite', 'priceless',
        'spectacular', 'stellar', 'talented', 'commendable', 'valuable', 'resilient', 'clever',
        'intelligent', 'bright', 'faithful', 'generous', 'respected', 'unbeatable', 'amused', 
        'relatable', 'unique', 'encouraged', 'devoted', 'forgiving', 'refreshing', 'steadfast', 
        'expert', 'engaging', 'legendary', 'enthused', 'beneficial', 'profitable', 'masterful', 
        'illustrious', 'wonderstruck', 'vivacious', 'jubilant', 'successful', 'innovative', 'charismatic',
        'fulfilled', 'amplified', 'celebrated', 'astounding', 'breathtaking', 'welcoming', 'warm', 
        'precious', 'stellar', 'alluring', 'pleasurable', 'harmonious', 'motivational', 'grateful',
        'sensational', 'funny', 'uplifting', 'resourceful', 'hopeful', 'cheery', 'forgiving', 'golden',
        'exemplary', 'influential'
    ]

    # Negative words
    negative_words = [
        'bad', 'terrible', 'awful', 'horrible', 'hate', 'worst', 'ugly', 'sad', 'disappointing', 'poor',
        'disgusting', 'pathetic', 'useless', 'unfavorable', 'negative', 'angry', 'furious', 'dreadful',
        'painful', 'unhappy', 'upset', 'depressing', 'annoying', 'frustrating', 'displeasing',
        'disturbing', 'unpleasant', 'regretful', 'hateful', 'filthy', 'repulsive', 'critical', 'mean',
        'insulting', 'disrespectful', 'offensive', 'inferior', 'problematic', 'weak', 'incompetent',
        'overwhelming', 'disastrous', 'disgraceful', 'pessimistic', 'disheartened', 'dreary', 'hurtful',
        'disjointed', 'worrying', 'detestable', 'lousy', 'lackluster', 'regrettable', 'painstaking',
        'troublesome', 'hostile', 'obnoxious', 'disadvantaged', 'stressed', 'dejected', 'miserable',
        'resentful', 'uncertain', 'unsteady', 'tense', 'jealous', 'envious', 'unsuccessful', 'bland',
        'oppressive', 'unlucky', 'loser', 'argumentative', 'nagging', 'brutal', 'bitter', 'cold', 'unfair',
        'vexed', 'melancholy', 'unimpressive', 'forgetful', 'neglectful', 'dismissive', 'unjust', 'hostility',
        'sorrowful', 'artificial', 'mindless', 'malicious', 'controlling', 'resentment', 'pained', 'suffer',
        'despair', 'intolerant', 'scared', 'depress', 'regret', 'stubborn', 'unfriendly', 'ignorant',
        'inconsiderate', 'wasteful', 'irrational', 'rude', 'worrisome', 'fake', 'hopeless', 'insensitive',
        'selfish', 'damaging', 'destructive', 'chaotic', 'immature', 'fearful', 'grim', 'cruel', 'shameful',
        'mad', 'burnout', 'rotten', 'useless', 'failure', 'ruined', 'awry', 'paranoid', 'guilty', 'jealousy',
        'condescending', 'abusive', 'sarcastic', 'hostile', 'inadequate', 'horrid', 'dreary', 'irate',
        'catastrophic', 'resent', 'offend', 'scornful', 'flawed', 'counterproductive', 'dumb', 'panic',
        'dissatisfied', 'hindrance', 'blocked', 'apathetic', 'weary', 'criticized', 'unapproachable'
    ]

    # Count occurences
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    # Determine sentiment
    if positive_count > negative_count:
        sentiment = "positive"
        total_count = positive_count + negative_count
        confidence = positive_count / total_count
        confidence = round(confidence, 2) if total_count > 0 else 0.5
    elif negative_count > positive_count:
        sentiment = "negative"
        total_count = negative_count + positive_count
        confidence = negative_count / total_count
        confidence = round(confidence, 2) if total_count > 0 else 0.5
    else:
        sentiment = "neutral"
        confidence = 0.5

    return sentiment, confidence

def estimate_reading_grade_level(word_count: int, sentence_count: int) -> float:
    # Validation check
    if word_count == 0 or sentence_count == 0:
        return 0

    # How many words are in a typical sentence?
    average_words_per_sentence = word_count / sentence_count

    # DENSITY: How many sentences are in a typical word
    average_sentences_per_word =sentence_count / word_count

    # Standard formula (LOOK THIS UP PLEASE 😂)
    score = (0.39 * average_words_per_sentence) + (11.8 * average_sentences_per_word) - 15.59

    # Ensuring we dont return a negative grade
    final_grade = max(0, score)
    return round(final_grade, 2)

def count_letter_types(text: str) -> tuple:
    # VOWELS - these are the a,e,i,o,u
    # CONSONANTS - all letters which are not vowels b,c,d,f

    text_lower = text.lower()

    vowel_count = sum(1 for letter in text_lower if letter in "aeiou")
    consonant_count = sum(1 for letter in text_lower if letter not in "aeiou")

    return vowel_count, consonant_count

def analyze_text(text: str) -> TextAnalysisResponse:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    # Clean text
    text = clean_text(text)

    # Get basic counts
    word_count = count_words(text)
    char_with_spaces, char_without_spaces = count_characters(text)
    sentence_count = count_sentences(text)

    # Get words list
    words = get_words_list(text)

    # Calculate metrics
    average_word_length = calculate_average_word_length(words)
    average_sentence_length = calculate_average_sentence_length(text, sentence_count)
    most_common_words = get_most_common_words(words)
    unique_words = count_unique_words(words)
    reading_time_minutes = calculate_reading_time(word_count)

    # Sentiment analysis
    sentiment, sentiment_confidence = sentiment_analyser(text)

    # Readability
    readability_score = estimate_reading_grade_level(word_count, sentence_count)

    # Count vowels & consonants
    vowels, consonants = count_letter_types(text)

    # Language statistics
    language_statistics = {
        "vowels": vowels,
        "consonants": consonants,
        "vowel_consonant_ratio": round(vowels/consonants, 2) if consonants > 0 else 0
    }

    return TextAnalysisResponse(
        word_count = word_count,
        character_count = char_with_spaces,
        character_count_no_spaces = char_without_spaces,
        sentence_count = sentence_count,
        average_word_length = average_word_length,
        average_sentence_length = average_sentence_length,
        most_common_words = most_common_words,
        unique_words = unique_words,
        reading_time_minutes = reading_time_minutes,
        sentiment = sentiment,
        sentiment_confidence = sentiment_confidence,
        readability_score = readability_score,
        language_statistics = language_statistics
    )

# API ENDPOINTS
@app.get("/")
def home():
    return {
        "message": "Welcome to the TEXT ANALYSIS API",
        "docs": "Visit http://localhost:8000/docs",
        "endpoints": [
            "/analyze/ - Analyze text and get detailed statistics",
            "/word-count/ - Count the number of words in a text",
            "/character-count/ - Count the number of characters in a text",
            "/sentence-count/ - Count the number of sentences in a text",
            "/sentiment/ - Analyze the sentiment of a text",
            "/readability/ - Estimate the readability of a text",
        ]
    }

@app.post("/analyze", response_model=TextAnalysisResponse)
def analyze_text_endpoint(text_input: TextInput):
    try:
        result = analyze_text(text_input.text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/word-count", response_model=SimpleResponse)
def word_count_endpoint(text_input: TextInput):
    try:
        text = clean_text(text_input.text)
        word_count = count_words(text)
        return SimpleResponse(result=word_count, unit="words")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/character-count", response_model=SimpleResponse)
def character_count_endpoint(text_input: TextInput):
    try:
        text = clean_text(text_input.text)
        char_with_spaces, char_without_spaces = count_characters(text)
        return {
            "with_spaces": char_with_spaces,
            "without_spaces": char_without_spaces,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sentence-count", response_model=SimpleResponse)
def sentence_count_endpoint(text_input: TextInput):
    try:
        text = clean_text(text_input.text)
        sentence_count = count_sentences(text)
        return SimpleResponse(result=sentence_count, unit="sentences")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sentiment")
def sentiment_endpoint(text_input: TextInput):
    try:
        text = clean_text(text_input.text)
        sentiment, confidence = sentiment_analyser(text)
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "message": f"The sentiment of the text is {sentiment} with a confidence of {confidence}",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/readability")
def readability_endpoint(text_input: TextInput):
    try:
        text = clean_text(text_input.text)
        word_count = count_words(text)
        sentence_count = count_sentences(text)
        readability_score = estimate_reading_grade_level(word_count, sentence_count)
        
        # Determine difficulty level
        if readability_score < 3:
            difficulty = "beginner"
        elif readability_score < 6:
            difficulty = "medium"
        elif readability_score < 9:
            difficulty = "advanced"
        else:
            difficulty = "expert"
        
        return {
            "readability_score": readability_score,
            "difficulty": difficulty,
            "message": f"The readability score of the text is {readability_score} and the difficulty level is {difficulty}",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/keywords")
def keywords_endpoint(text_input: TextInput):
    try:
        text = clean_text(text_input.text)
        words = get_words_list(text)
        most_common_words = get_most_common_words(words)
        return {
            "keywords": most_common_words,
            "count": len(most_common_words),
            "message": f"The most common words in the text are {most_common_words}",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/summary")
def summary_endpoint(text_input: TextInput):
    try:
        result = analyze_text(text_input.text)

        return {
            "summary":{
                "words": result.word_count,
                "characters": result.character_count,
                "sentences": result.sentence_count,
                "average_word_length": result.average_word_length,
                "average_sentence_length": result.average_sentence_length,
                "most_common_words": result.most_common_words,
                "top_word": result.most_common_words[:1],
                "unique_words": result.unique_words,
                "reading_time_minutes": result.reading_time_minutes,
                "sentiment": result.sentiment,
                "readability_score": result.readability_score,
                "language_statistics": result.language_statistics,
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ERROR HANDLING
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return HTTPException(status_code=400, detail=str(exc))