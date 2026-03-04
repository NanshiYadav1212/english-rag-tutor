# Unified RAG Backend (single file)
# This file merges all logic: memory, chunking, embeddings, LLM, loaders, prompts, vector store, API, and FastAPI app.

from collections import defaultdict, deque
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import fitz, docx
import requests
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# --- Memory (chat history) ---
memory = defaultdict(lambda: deque(maxlen=6))
def add(user, course, role, msg):
    memory[f"{user}-{course}"].append({"role": role, "msg": msg})
def get(user, course):
    return list(memory[f"{user}-{course}"])

# --- Chunking ---
def chunk_text(text, size=500, overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunks.append(" ".join(words[i:i+size]))
    return chunks

# --- Embeddings ---
_embedder = None
def get_embedder():
    global _embedder
    if _embedder is None:
        print("Loading embedding model...")
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder
def embed_chunks(chunks):
    model = get_embedder()
    embeddings = model.encode(chunks).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings

# --- LLM (Gemini API) ---
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
def generate(prompt):
    if not API_KEY:
        print(f"ERROR: API Key not found. Checking path: {BASE_DIR / '.env'}")
        raise ValueError("Please set GEMINI_API_KEY in your .env file")
    url = f"{API_URL}?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 2048, "temperature": 0.4}
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"!!! GEMINI API ERROR: {response.status_code} - {response.text}")
            return "I'm sorry, I'm having trouble connecting to my brain right now."
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"!!! CRITICAL SYSTEM ERROR: {str(e)}")
        return "System error: Failed to process the request."

# --- File Loaders ---
def extract_text(file):
    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=file.file.read(), filetype="pdf")
        return "".join(page.get_text() for page in doc)
    if file.filename.endswith(".docx"):
        d = docx.Document(file.file)
        return "\n".join(p.text for p in d.paragraphs)
    return file.file.read().decode("utf-8")

# --- Prompt Template ---
def qna_prompt(context, question, history):
    chat = "\n".join(f"{h['role']}: {h['msg']}" for h in history)
    return f"""
### ROLE
You are an Advanced AI Academic Tutor. You provide deeply expanded, structured, and professional responses.

### MODE 1: DOCUMENT-BASED Q&A
- If the student asks a question: Use the \"Learning Context\" as the primary source.
- If the information is not in the context, use your own external knowledge to provide a full explanation.
- **CRITICAL**: You MUST prefix any information NOT found in the document with: **\"[External Knowledge]:\"**.

### MODE 2: QUIZ GENERATION
- If the student asks to \"Generate questions\" (e.g., \"Generate 5 questions with answers\"):
- You MUST use ONLY the \"Learning Context\" provided below. Do NOT use external information.
- Provide a mix of multiple-choice and descriptive questions.
- Provide a detailed \"Answer Key\" at the bottom.

### FORMATTING RULES:
- Use **Markdown** headers (###) for sections.
- Use **bold text** for key terminology.
- Use bullet points for readability.

---
### LEARNING CONTEXT:
{context}

---
### STUDENT QUESTION:
{question}

### DETAILED RESPONSE:
"""

# --- Vector Store ---
def _paths(user_id, course_id):
    base = f"vector_db/user_{user_id}/course_{course_id}"
    os.makedirs(base, exist_ok=True)
    return f"{base}/index.faiss", f"{base}/chunks.pkl"
def save_index(index, chunks, user_id, course_id):
    i, c = _paths(user_id, course_id)
    faiss.write_index(index, i)
    pickle.dump(chunks, open(c, "wb"))
def load_index(user_id, course_id):
    i, c = _paths(user_id, course_id)
    return faiss.read_index(i), pickle.load(open(c, "rb"))

# --- RAG Engine ---
embedder = get_embedder()
def ask_rag(user_id, course_id, question):
    index, chunks = load_index(user_id, course_id)
    q_emb = embedder.encode([question]).astype("float32")
    _, ids = index.search(q_emb, 3)
    context = "\n".join(chunks[i] for i in ids[0])
    history = get(user_id, course_id)
    prompt = qna_prompt(context, question, history)
    answer = generate(prompt)
    add(user_id, course_id, "user", question)
    add(user_id, course_id, "assistant", answer)
    return answer

# --- FastAPI App & Endpoints ---
router = APIRouter()
USER_ID = "single_user"
COURSE_ID = "default_course"

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    text = extract_text(file)
    chunks = chunk_text(text)
    index, embeddings = embed_chunks(chunks)
    save_index(index, chunks, USER_ID, COURSE_ID)
    return {"status": "Knowledge base updated!"}

@router.post("/ask")
async def ask(question: str):
    answer = ask_rag(USER_ID, COURSE_ID, question)
    return {"answer": answer}

app = FastAPI(title="Personal RAG Assistant (Unified)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
