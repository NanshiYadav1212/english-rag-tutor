# from fastapi import APIRouter, UploadFile
# from app.rag.loaders import extract_text
# from app.rag.chunker import chunk_text
# from app.rag.embeddings import embed_chunks
# from app.rag.vector_store import save_index
# from app.rag.rag_engine import ask_rag

# router = APIRouter()

# @router.post("/upload")
# async def upload_file(user_id: int, course_id:int, file:UploadFile):
#     text = extract_text(file)
#     chunks = chunk_text(text)
#     index, embeddings = embed_chunks(chunks)
#     save_index(index,chunks,user_id,course_id)
#     return {"status": "Document indexed"}

# @router.post("/ask")
# async def ask(user_id:int,course_id:int,question:str):
#     answer = ask_rag(user_id,course_id,question)
#     return {"answer":answer}
    
    
    
# from fastapi import APIRouter, UploadFile, File
# from app.rag.rag_engine import ask_rag
# from app.rag.loaders import extract_text
# from app.rag.chunker import chunk_text
# from app.rag.embeddings import embed_chunks
# from app.rag.vector_store import save_index

# router = APIRouter()
# DEFAULT_ID = "my_knowledge_base" # Simplified ID for a single user

# @router.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     text = extract_text(file)
#     chunks = chunk_text(text)
#     index, embeddings = embed_chunks(chunks)
#     # Hardcoding the ID saves the index into a single predictable folder
#     save_index(index, chunks, DEFAULT_ID, DEFAULT_ID)
#     return {"status": "Document indexed successfully"}

# @router.post("/ask")
# async def ask(question: str):
#     # Using the same hardcoded ID to retrieve the correct context
#     answer = ask_rag(DEFAULT_ID, DEFAULT_ID, question)
#     return {"answer": answer}



from fastapi import APIRouter, UploadFile, File
from app.rag.rag_engine import ask_rag
from app.rag.loaders import extract_text
from app.rag.chunker import chunk_text
from app.rag.embeddings import embed_chunks
from app.rag.vector_store import save_index

router = APIRouter()
# This replaces the dynamic IDs to simplify your personal storage
USER_ID = "single_user"
COURSE_ID = "default_course"

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    text = extract_text(file)
    chunks = chunk_text(text)
    index, embeddings = embed_chunks(chunks)
    # Saves to vector_db/user_single_user/course_default_course/
    save_index(index, chunks, USER_ID, COURSE_ID)
    return {"status": "Knowledge base updated!"}

@router.post("/ask")
async def ask(question: str):
    # Retrieve from the same hardcoded location
    answer = ask_rag(USER_ID, COURSE_ID, question)
    return {"answer": answer}