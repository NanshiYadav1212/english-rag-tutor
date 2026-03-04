from fastapi import APIRouter, HTTPException
from app.db import db
from bson import ObjectId

router = APIRouter()


def serialize_doc(doc):
    """Convert MongoDB documents to JSON-serializable format"""
    if not doc:
        return None
    if isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, dict):
        return {k: serialize_doc(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_doc(i) for i in doc]
    return doc


@router.get("/")
async def list_lessons():
    """Get all lessons with metadata (no detailed notes)"""
    try:
        lessons = list(db['lessons'].find({}))
        return [serialize_doc(l) for l in lessons]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lessons: {str(e)}")


@router.get("/{slug}")
async def get_lesson(slug: str):
    lesson = db['lessons'].find_one({"slug": slug})
    if not lesson:
        return {"error": "Lesson not found"}
    return serialize_doc(lesson)
