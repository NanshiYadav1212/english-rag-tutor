# from fastapi import APIRouter, HTTPException, Request
# from ..db import db
# from datetime import datetime
# from pydantic import BaseModel, ValidationError
# from typing import List, Dict, Any, Optional
# from bson import ObjectId
# import json

# router = APIRouter()


# # ================= MODELS =================

# class QuizAnswer(BaseModel):
#     question_id: str
#     answer: Any


# class QuizSubmission(BaseModel):
#     lesson_slug: str
#     quiz_type: str
#     answers: List[QuizAnswer]
#     user_email: Optional[str] = None
#     time_taken: Optional[float] = None


# def build_answers_map(answers_list: List[QuizAnswer]) -> Dict[str, Any]:
#     return {a.question_id: a.answer for a in answers_list}


# def serialize_doc(doc):
#     if not doc:
#         return None
#     if isinstance(doc, ObjectId):
#         return str(doc)
#     if isinstance(doc, dict):
#         return {k: serialize_doc(v) for k, v in doc.items()}
#     if isinstance(doc, list):
#         return [serialize_doc(i) for i in doc]
#     return doc


# # ================= QUIZ GET =================

# # @router.get("/quiz/{lesson_slug}/{quiz_type}")

# @router.get("/{lesson_slug}/{quiz_type}")
# async def get_quiz_by_type(lesson_slug: str, quiz_type: str):

#     # quiz_doc = db["quizzes"].find_one({"lesson_slug": lesson_slug})
#     quiz_doc = db["quizzes_questions"].find_one({"lesson_slug": lesson_slug})
#     if not quiz_doc:
#         raise HTTPException(404, "Quiz not found")

#     # quiz_type_data = quiz_doc.get("quiz_types", {}).get(quiz_type)
#     # quiz_type_data = quiz_doc.get("quiz_types", {}).get(quiz_type)
#     if not quiz_type_data:
#         raise HTTPException(404, "Quiz type not found")

#     questions_clean = []
#     for q in quiz_type_data.get("questions", []):
#         q_clean = {
#             k: v for k, v in q.items()
#             if k not in ["correct_answer", "explanation"]
#         }
#         questions_clean.append(q_clean)

#     return {
#         "lesson_slug": lesson_slug,
#         "quiz_type": quiz_type,
#         "questions": questions_clean
#     }


# # ================= SUBMIT =================

# # @router.post("/submit")
# # async def submit_quiz(request: Request):

# #     try:
# #         raw_data = await request.json()
# #         payload = QuizSubmission(**raw_data)

# #         lesson = db["lessons"].find_one({"slug": payload.lesson_slug})
# #         if not lesson:
# #             raise HTTPException(404, "Lesson not found")

# #         quiz_doc = db["quizzes"].find_one({"lesson_slug": payload.lesson_slug})
# #         quiz_type_data = quiz_doc["quiz_types"][payload.quiz_type]

# #         questions = quiz_type_data["questions"]
# #         answers_map = build_answers_map(payload.answers)

# #         total_marks = sum(q.get("marks", 1) for q in questions)

# #         score = 0
# #         detailed_results = []

# #         for q in questions:
# #             qid = str(q["question_id"])
# #             user_answer = answers_map.get(qid)
# #             correct_answer = q.get("correct_answer")

# #             is_correct = str(user_answer).lower().strip() == \
# #                          str(correct_answer).lower().strip()

# #             marks = q.get("marks", 1) if is_correct else 0
# #             score += marks

# #             detailed_results.append({
# #                 "question_id": qid,
# #                 "user_answer": user_answer,
# #                 "correct_answer": correct_answer,
# #                 "is_correct": is_correct,
# #                 "marks": marks
# #             })

# #         percentage = round((score / total_marks) * 100, 2)

# #         db["quiz_attempts"].insert_one({
# #             "lesson_slug": payload.lesson_slug,
# #             "quiz_type": payload.quiz_type,
# #             "percentage": percentage,
# #             "score": score,
# #             "total": total_marks,
# #             "submitted_at": datetime.utcnow(),
# #             "user_email": payload.user_email or "anonymous@local"
# #         })

# #         return {
# #             "success": True,
# #             "percentage": percentage,
# #             "score": score,
# #             "total": total_marks,
# #             "details": detailed_results
# #         }

# #     except ValidationError as e:
# #         raise HTTPException(422, str(e))
# #     except Exception as e:
# #         raise HTTPException(500, str(e))
# # ================= GET FULL LESSON QUIZ =================

# # @router.get("/quiz/lesson/{lesson_slug}")
# # async def get_full_lesson_quiz(lesson_slug: str):

# #     quiz_doc = db["quizzes"].find_one({"lesson_slug": lesson_slug})

# #     if not quiz_doc:
# #         raise HTTPException(404, "Quiz not found")

# #     quiz_types_clean = {}

# #     for quiz_type, quiz_data in quiz_doc.get("quiz_types", {}).items():

# #         cleaned_questions = []

# #         for q in quiz_data.get("questions", []):

# #             q_clean = {
# #                 k: v for k, v in q.items()
# #                 if k not in ["correct_answer", "explanation"]
# #             }

# #             cleaned_questions.append(q_clean)

# #         quiz_types_clean[quiz_type] = {
# #             "questions": cleaned_questions,
# #             "total_questions": len(cleaned_questions)
# #         }

# #     return {
# #         "lesson_slug": lesson_slug,
# #         "lesson_title": quiz_doc.get("lesson_title", lesson_slug),
# #         "quiz_types": quiz_types_clean
# #     }

# # @router.get("/quiz/lesson/{lesson_slug}")

# @router.get("/lesson/{lesson_slug}")
# async def get_full_lesson_quiz(lesson_slug: str):

#     quiz_doc = db["quizzes_questions"].find_one({"lesson_slug": lesson_slug})

#     if not quiz_doc:
#         raise HTTPException(404, "Quiz not found")

#     quiz_types_clean = {}

#     for quiz_type, quiz_data in quiz_doc.get("quiz_types", {}).items():

#         cleaned_questions = []

#         for q in quiz_data.get("questions", []):

#             q_clean = {
#                 k: v for k, v in q.items()
#                 if k not in ["correct_answer", "explanation"]
#             }

#             cleaned_questions.append(q_clean)

#         quiz_types_clean[quiz_type] = {
#             "questions": cleaned_questions,
#             "total_questions": len(cleaned_questions)
#         }

#     return {
#         "lesson_slug": lesson_slug,
#         "lesson_title": quiz_doc.get("lesson_title", lesson_slug),
#         "quiz_types": quiz_types_clean
#     }

# # ================= QUIZ ATTEMPTS =================

# @router.get("/attempts/{lesson_slug}")
# async def get_attempts(lesson_slug: str):

#     attempts = list(
#         db["quiz_attempts"].find(
#             {"lesson_slug": lesson_slug},
#             {"_id": 0}
#         )
#     )

#     return {
#         "lesson_slug": lesson_slug,
#         "attempts": attempts
#     }






#--------------------changing this code 

from fastapi import APIRouter, HTTPException, Request
from ..db import db
from datetime import datetime
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any, Optional
from bson import ObjectId

router = APIRouter()


# ================= MODELS =================

class QuizAnswer(BaseModel):
    question_id: str
    answer: Any


class QuizSubmission(BaseModel):
    lesson_slug: str
    quiz_type: str
    answers: List[QuizAnswer]
    user_email: Optional[str] = None
    time_taken: Optional[float] = None


def build_answers_map(answers_list: List[QuizAnswer]) -> Dict[str, Any]:
    return {a.question_id: a.answer for a in answers_list}


def serialize_doc(doc):
    if not doc:
        return None

    if isinstance(doc, ObjectId):
        return str(doc)

    if isinstance(doc, dict):
        return {k: serialize_doc(v) for k, v in doc.items()}

    if isinstance(doc, list):
        return [serialize_doc(i) for i in doc]

    return doc


# ================= GET FULL LESSON QUIZ =================

@router.get("/lesson/{lesson_slug}")
async def get_full_lesson_quiz(lesson_slug: str):

    quiz_docs = list(
        db["quiz_questions"].find(
            {"lesson_slug": lesson_slug},
            {"_id": 0}
        )
    )

    if not quiz_docs:
        raise HTTPException(404, "Quiz not found")

    quiz_types_clean = {}

    for quiz_doc in quiz_docs:

        quiz_type = quiz_doc["quiz_type"]

        cleaned_questions = []

        for q in quiz_doc.get("questions", []):

            q_clean = {
                k: v for k, v in q.items()
                if k not in ["correct_answer", "explanation"]
            }

            cleaned_questions.append(q_clean)

        quiz_types_clean[quiz_type] = {
            "questions": cleaned_questions,
            "total_questions": len(cleaned_questions)
        }

    return {
        "lesson_slug": lesson_slug,
        "lesson_title": quiz_docs[0].get(
            "lesson_title",
            lesson_slug
        ),
        "quiz_types": quiz_types_clean
    }



# ================= GET QUIZ BY TYPE =================

@router.get("/{lesson_slug}/{quiz_type}")
async def get_quiz_by_type(lesson_slug: str, quiz_type: str):

    quiz_doc = db["quiz_questions"].find_one({
        "lesson_slug": lesson_slug,
        "quiz_type": quiz_type
    })

    if not quiz_doc:
        raise HTTPException(404, "Quiz not found")

    questions_clean = []

    for q in quiz_doc.get("questions", []):

        q_clean = {
            k: v for k, v in q.items()
            if k not in ["correct_answer", "explanation"]
        }

        questions_clean.append(q_clean)

    return {
        "lesson_slug": lesson_slug,
        "quiz_type": quiz_type,
        "questions": questions_clean
    }


# ================= SUBMIT QUIZ =================

@router.post("/submit")
async def submit_quiz(request: Request):

    try:

        raw_data = await request.json()
        payload = QuizSubmission(**raw_data)

        lesson = db["lessons"].find_one({
            "slug": payload.lesson_slug
        })

        if not lesson:
            raise HTTPException(404, "Lesson not found")

        quiz_doc = db["quiz_questions"].find_one({
            "lesson_slug": payload.lesson_slug,
            "quiz_type": payload.quiz_type
        })

        if not quiz_doc:
            raise HTTPException(404, "Quiz not found")

        questions = quiz_doc.get("questions", [])

        answers_map = build_answers_map(payload.answers)

        total_marks = sum(
            q.get("marks", 1)
            for q in questions
        )

        score = 0

        detailed_results = []

        for q in questions:

            qid = str(q["question_id"])

            user_answer = answers_map.get(qid)

            correct_answer = q.get("correct_answer")

            is_correct = (
                str(user_answer).lower().strip()
                ==
                str(correct_answer).lower().strip()
            )

            marks = q.get("marks", 1) if is_correct else 0

            score += marks

            detailed_results.append({
                "question_id": qid,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "marks": marks
            })

        percentage = round(
            (score / total_marks) * 100,
            2
        )

        db["quiz_attempts"].insert_one({
            "lesson_slug": payload.lesson_slug,
            "quiz_type": payload.quiz_type,
            "percentage": percentage,
            "score": score,
            "total": total_marks,
            "submitted_at": datetime.utcnow(),
            "user_email": payload.user_email or "anonymous@local"
        })

        return {
            "success": True,
            "percentage": percentage,
            "score": score,
            "total": total_marks,
            "details": detailed_results
        }

    except ValidationError as e:
        raise HTTPException(422, str(e))

    except Exception as e:
        raise HTTPException(500, str(e))


# # ================= GET FULL LESSON QUIZ =================

# @router.get("/lesson/{lesson_slug}")
# async def get_full_lesson_quiz(lesson_slug: str):

#     quiz_docs = list(
#         db["quiz_questions"].find(
#             {"lesson_slug": lesson_slug},
#             {"_id": 0}
#         )
#     )

#     if not quiz_docs:
#         raise HTTPException(404, "Quiz not found")

#     quiz_types_clean = {}

#     for quiz_doc in quiz_docs:

#         quiz_type = quiz_doc["quiz_type"]

#         cleaned_questions = []

#         for q in quiz_doc.get("questions", []):

#             q_clean = {
#                 k: v for k, v in q.items()
#                 if k not in ["correct_answer", "explanation"]
#             }

#             cleaned_questions.append(q_clean)

#         quiz_types_clean[quiz_type] = {
#             "questions": cleaned_questions,
#             "total_questions": len(cleaned_questions)
#         }

#     return {
#         "lesson_slug": lesson_slug,
#         "lesson_title": quiz_docs[0].get(
#             "lesson_title",
#             lesson_slug
#         ),
#         "quiz_types": quiz_types_clean
#     }


# ================= QUIZ ATTEMPTS =================

@router.get("/attempts/{lesson_slug}")
async def get_attempts(lesson_slug: str):

    attempts = list(
        db["quiz_attempts"].find(
            {"lesson_slug": lesson_slug},
            {"_id": 0}
        )
    )

    return {
        "lesson_slug": lesson_slug,
        "attempts": attempts
    }