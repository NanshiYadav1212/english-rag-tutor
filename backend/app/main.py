import os
import warnings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
import logging

logger = logging.getLogger(__name__)

# ---- Silence unnecessary logs ----
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ---- App initialization ----
app = FastAPI(title="AI Language Tutor API")

# ---- Startup tasks ----
from app.db import init_db

@app.on_event("startup")
async def startup_event():
    try:
        init_db()
    except Exception as e:
        logger.error(f"init_db failed: {e}")
        

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Include routers ----
from app.routes import auth, lessons, exercises, progress, quiz, quiz_submit

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(lessons.router, prefix="/api/lessons", tags=["lessons"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["quiz"])
app.include_router(quiz_submit.router, prefix="/api/quiz", tags=["quiz"])

# ---- Smart Tutor / RAG routes ----
from app.api import router as rag_router
app.include_router(rag_router, tags=["smart-tutor"])

