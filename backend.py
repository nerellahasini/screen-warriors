import os
from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from jose import jwt
from dotenv import load_dotenv
from groq import Groq

# ==============================
# Environment Setup
# ==============================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./researchhub.db")

ALGORITHM = "HS256"

# ==============================
# Database Setup
# ==============================

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ==============================
# Models
# ==============================

class User(Base):
    _tablename_ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Paper(Base):
    _tablename_ = "papers"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    authors = Column(String)
    abstract = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))

Base.metadata.create_all(bind=engine)

# ==============================
# Security
# ==============================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ==============================
# Groq Setup
# ==============================

client = Groq(api_key=GROQ_API_KEY)

MODEL_CONFIG = {
    "model": "llama-3.3-70b-versatile",
    "temperature": 0.3,
    "max_tokens": 1500,
    "top_p": 0.9
}

# ==============================
# FastAPI App
# ==============================

app = FastAPI(title="ResearchHub AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Dependency
# ==============================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==============================
# Authentication APIs
# ==============================

@app.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(password)
    user = User(email=email, password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# ==============================
# Paper Search API (Demo)
# ==============================

@app.get("/search")
def search_papers(query: str):
    # Replace with real API like arXiv later
    return {
        "papers": [
            {
                "title": "Transformer vs CNN Architectures",
                "authors": "John Doe",
                "abstract": "This paper compares transformer and CNN architectures..."
            }
        ]
    }

# ==============================
# Import Paper
# ==============================

@app.post("/import")
def import_paper(title: str, authors: str, abstract: str,
                 owner_id: int, db: Session = Depends(get_db)):

    paper = Paper(
        title=title,
        authors=authors,
        abstract=abstract,
        owner_id=owner_id
    )
    db.add(paper)
    db.commit()

    return {"message": "Paper imported successfully"}

# ==============================
# AI Chatbot
# ==============================

@app.post("/chat")
async def chat(message: str):

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert research assistant."},
            {"role": "user", "content": message}
        ],
        **MODEL_CONFIG
    )

    return {"response": response.choices[0].message.content}

# ==============================
# Root
# ==============================

@app.get("/")
def root():
    return {"message": "ResearchHub AI API is running"}