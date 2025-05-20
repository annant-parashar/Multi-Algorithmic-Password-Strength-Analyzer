from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import string
import re
import math
from typing import List

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Common password list (sample)
COMMON_PASSWORDS = {
    "password", "123456", "qwerty", "admin", "letmein", "welcome",
    "monkey", "dragon", "baseball", "football", "secret", "abc123"
}

class PasswordRequest(BaseModel):
    password: str

class AnalysisResponse(BaseModel):
    length_score: float
    complexity_score: float
    dictionary_score: float
    bruteforce_score: float
    total_score: float
    suggestions: List[str]

class PasswordResponse(BaseModel):
    password: str

def calculate_length_score(password: str) -> float:
    length = len(password)
    if length < 8: return 0
    if length < 12: return 0.5
    if length < 16: return 0.75
    return 1

def calculate_complexity_score(password: str) -> float:
    score = 0
    if re.search(r'[A-Z]', password): score += 0.25  # Uppercase
    if re.search(r'[a-z]', password): score += 0.25  # Lowercase
    if re.search(r'[0-9]', password): score += 0.25  # Numbers
    if re.search(r'[^A-Za-z0-9]', password): score += 0.25  # Special chars
    return score

def calculate_dictionary_score(password: str) -> float:
    if password.lower() in COMMON_PASSWORDS:
        return 0
    return 1

def calculate_bruteforce_score(password: str) -> float:
    charset_size = 0
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[0-9]', password): charset_size += 10
    if re.search(r'[^A-Za-z0-9]', password): charset_size += 32
    
    combinations = math.pow(max(charset_size, 1), len(password))
    guesses_per_second = 1000000000  # Assume 1 billion guesses per second
    seconds = combinations / guesses_per_second
    
    if seconds < 3600: return 0  # Less than an hour
    if seconds < 86400: return 0.25  # Less than a day
    if seconds < 2592000: return 0.5  # Less than a month
    if seconds < 31536000: return 0.75  # Less than a year
    return 1

def generate_suggestions(
    password: str,
    length_score: float,
    complexity_score: float,
    dictionary_score: float,
    bruteforce_score: float
) -> List[str]:
    suggestions = []
    
    if length_score < 1:
        suggestions.append("Make your password longer (16+ characters recommended)")
    
    if complexity_score < 1:
        if not re.search(r'[A-Z]', password):
            suggestions.append("Add uppercase letters")
        if not re.search(r'[a-z]', password):
            suggestions.append("Add lowercase letters")
        if not re.search(r'[0-9]', password):
            suggestions.append("Add numbers")
        if not re.search(r'[^A-Za-z0-9]', password):
            suggestions.append("Add special characters")
    
    if dictionary_score < 1:
        suggestions.append("Avoid common passwords")
    
    if bruteforce_score < 0.5:
        suggestions.append("Increase complexity to resist brute-force attacks")
    
    return suggestions

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_password(request: PasswordRequest):
    password = request.password
    
    length_score = calculate_length_score(password)
    complexity_score = calculate_complexity_score(password)
    dictionary_score = calculate_dictionary_score(password)
    bruteforce_score = calculate_bruteforce_score(password)
    
    total_score = (length_score + complexity_score + dictionary_score + bruteforce_score) / 4
    
    suggestions = generate_suggestions(
        password,
        length_score,
        complexity_score,
        dictionary_score,
        bruteforce_score
    )
    
    return AnalysisResponse(
        length_score=length_score,
        complexity_score=complexity_score,
        dictionary_score=dictionary_score,
        bruteforce_score=bruteforce_score,
        total_score=total_score,
        suggestions=suggestions
    )

def generate_strong_password(length: int = 16) -> str:
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character from each category
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill the rest randomly
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(length - 4))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

@app.get("/generate", response_model=PasswordResponse)
async def generate_password():
    return PasswordResponse(password=generate_strong_password())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
