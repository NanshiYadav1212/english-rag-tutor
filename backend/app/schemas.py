# from pydantic import BaseModel
# from typing import Optional

# class ExerciseSubmit(BaseModel):
#     lesson_id: str        # ← Changed from int to str
#     user_input: str
#     mode: Optional[str] = 'free_text'

from pydantic import BaseModel
from typing import Optional

class ExerciseSubmit(BaseModel):
    lesson_id: str
    user_input: str
    mode: Optional[str] = 'free_text'
