from pydantic import BaseModel
from typing import Optional, List, Dict

class User(BaseModel):
    email: str
    hashed_password: str
    level: str = "beginner"
    recommended_path: Optional[List[str]] = []
    created_at: Optional[str] = None


class ExerciseResult(BaseModel):
    user_email: str
    lesson_id: str
    user_input: str
    evaluation: Dict
    submitted_at: Optional[str] = None
    favorite: bool = False
