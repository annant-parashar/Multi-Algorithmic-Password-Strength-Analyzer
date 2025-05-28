from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import random
import string
import re
import math
import os
from typing import List

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for vault
VAULT_DIR = "vault_files"
VAULT_PASSWORD = "rootuser123#"
os.makedirs(VAULT_DIR, exist_ok=True)

# Common password list (sample)
COMMON_PASSWORDS = {
    "password", "123456", "qwerty", "admin", "letmein", "welcome",
    "monkey", "dragon", "baseball", "football", "secret", "abc123",
    "name123", "p@ssword", "111111", "987654321", "1223334444", "iloveyou",
    "hello123", "dragon", "batman", "google", "welcome123", "marvels", "1g2w3e4r"
}

# Models
class PasswordRequest(BaseModel):
    password: str

class AnalysisResponse(BaseModel):
    length_score: float
    complexity_score: float
    dictionary_score: float
    bruteforce_score: float
    total_score: float
    suggestions: List[str]
    redirectToSecureUpload: bool = False

class PasswordResponse(BaseModel):
    password: str

# Password strength calculation
def calculate_length_score(password: str) -> float:
    length = len(password)
    if length < 8: return 0
    if length < 12: return 0.5
    if length < 16: return 0.75
    return 1

def calculate_complexity_score(password: str) -> float:
    score = 0
    if re.search(r'[A-Z]', password): score += 0.25
    if re.search(r'[a-z]', password): score += 0.25
    if re.search(r'[0-9]', password): score += 0.25
    if re.search(r'[^A-Za-z0-9]', password): score += 0.25
    return score

def calculate_dictionary_score(password: str) -> float:
    return 0 if password.lower() in COMMON_PASSWORDS else 1

def calculate_bruteforce_score(password: str) -> float:
    charset_size = 0
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[0-9]', password): charset_size += 10
    if re.search(r'[^A-Za-z0-9]', password): charset_size += 32
    combinations = math.pow(max(charset_size, 1), len(password))
    guesses_per_second = 1_000_000_000
    seconds = combinations / guesses_per_second
    if seconds < 3600: return 0
    if seconds < 86400: return 0.25
    if seconds < 2592000: return 0.5
    if seconds < 31536000: return 0.75
    return 1

def generate_suggestions(password: str, length_score: float,
                         complexity_score: float,
                         dictionary_score: float,
                         bruteforce_score: float) -> List[str]:
    suggestions = []
    if length_score < 1:
        suggestions.append("Make your password longer (16+ characters recommended)")
    if complexity_score < 1:
        if not re.search(r'[A-Z]', password): suggestions.append("Add uppercase letters")
        if not re.search(r'[a-z]', password): suggestions.append("Add lowercase letters")
        if not re.search(r'[0-9]', password): suggestions.append("Add numbers")
        if not re.search(r'[^A-Za-z0-9]', password): suggestions.append("Add special characters")
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
    suggestions = generate_suggestions(password, length_score, complexity_score, dictionary_score, bruteforce_score)

    redirect = password == VAULT_PASSWORD

    return AnalysisResponse(
        length_score=length_score,
        complexity_score=complexity_score,
        dictionary_score=dictionary_score,
        bruteforce_score=bruteforce_score,
        total_score=total_score,
        suggestions=suggestions,
        redirectToSecureUpload=redirect
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), password: str = Form(...)):
    if password != VAULT_PASSWORD:
        # Wrong password: delete all files
        for f in os.listdir(VAULT_DIR):
            os.remove(os.path.join(VAULT_DIR, f))
        return JSONResponse(status_code=403, content={"message": "Incorrect password. Vault wiped."})

    save_path = os.path.join(VAULT_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": "File uploaded securely."}

@app.get("/vault")
async def list_vault(password: str):
    if password != VAULT_PASSWORD:
        for f in os.listdir(VAULT_DIR):
            os.remove(os.path.join(VAULT_DIR, f))
        raise HTTPException(status_code=403, detail="Incorrect password. Vault wiped.")
    return {"files": os.listdir(VAULT_DIR)}

@app.get("/generate", response_model=PasswordResponse)
async def generate_password():
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(12))
    random.shuffle(password)
    return PasswordResponse(password=''.join(password))
