from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import Dict, Any

from app.dependencies.auth import get_current_user
from app.database.mongodb import db

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/")
async def get_progress(user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get user's learning progress and statistics.
    """

    try:
        user_id = str(user["_id"])

        # Fetch progress document
        progress = await db.progress.find_one({"user_id": user_id})

        if not progress:
            # Default progress if not exists
            progress = {
                "user_id": user_id,
                "total_sessions": 0,
                "total_questions": 0,
                "correct_answers": 0,
                "accuracy": 0,
                "last_updated": datetime.utcnow(),
            }

            await db.progress.insert_one(progress)

        # Calculate accuracy safely
        total_questions = progress.get("total_questions", 0)
        correct_answers = progress.get("correct_answers", 0)

        accuracy = (
            (correct_answers / total_questions) * 100
            if total_questions > 0
            else 0
        )

        response = {
            "total_sessions": progress.get("total_sessions", 0),
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy": round(accuracy, 2),
            "last_updated": progress.get("last_updated"),
        }

        return {
            "success": True,
            "data": response,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching progress: {str(e)}",
        )

