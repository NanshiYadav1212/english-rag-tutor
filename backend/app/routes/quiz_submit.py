"""
Complete Quiz Submission & Grading System with ML Integration
Handles quiz submission, grading, progress tracking, and learning path prediction
"""
import logging

logger = logging.getLogger(__name__)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..db import db
from datetime import datetime, timedelta
from ..ml.level_predictor import predict_learning_path
from ..services.student_metrics import get_user_metrics
import numpy as np

router = APIRouter()


# ===== Pydantic Models =====
class QuestionAnswer(BaseModel):
    question_id: int
    user_answer: Any


class QuizSubmissionPayload(BaseModel):
    lesson_slug: str
    quiz_type: str
    answers: Dict[int, Any]  # {question_id: answer}
    user_email: Optional[str] = "anonymous@local"
    time_taken: Optional[float] = None


class QuizGradingResponse(BaseModel):
    lesson_slug: str
    quiz_type: str
    score_earned: int
    total_marks: int
    percentage: float
    passed: bool
    detailed_results: List[Dict[str, Any]]
    attempt_number: int
    lesson_completed: bool


# ===== Helper Functions =====
def serialize_doc(doc):
    """Convert MongoDB documents to JSON-serializable format"""
    if not doc:
        return None
    if isinstance(doc, dict):
        from bson import ObjectId
        return {k: str(v) if isinstance(v, ObjectId) else serialize_doc(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_doc(i) for i in doc]
    return doc


def calculate_score(payload: QuizSubmissionPayload, quiz_doc: Dict) -> tuple:
    """
    Grade quiz based on quiz type and return (score, total_marks, detailed_results)
    """
    quiz_type_data = quiz_doc.get('quiz_types', {}).get(payload.quiz_type)
    if not quiz_type_data:
        raise HTTPException(status_code=404, detail=f"Quiz type '{payload.quiz_type}' not found")
    
    questions = quiz_type_data.get('questions', [])
    total_marks = sum(q.get('marks', 1) for q in questions)
    
    score = 0
    detailed_results = []
    
    # Use answers dict directly
    user_answers_map = payload.answers
    
    for q in questions:
        q_id = q.get('question_id')
        user_answer = user_answers_map.get(q_id)
        correct_answer = q.get('correct_answer')
        marks_awarded = 0
        is_correct = False
        
        if user_answer is None:
            detailed_results.append({
                'question_id': q_id,
                'user_answer': None,
                'correct_answer': correct_answer,
                'is_correct': False,
                'marks_awarded': 0
            })
            continue
        
        # Grade based on quiz type
        if payload.quiz_type == 'multiple_choice':
            is_correct = user_answer == correct_answer
            marks_awarded = q.get('marks', 1) if is_correct else 0
            
        elif payload.quiz_type == 'true_false':
            # Handle string/boolean conversion
            if isinstance(user_answer, str):
                user_answer_bool = user_answer.lower() in ['true', 'yes', '1']
            else:
                user_answer_bool = bool(user_answer)
            is_correct = user_answer_bool == correct_answer
            marks_awarded = q.get('marks', 1) if is_correct else 0
            
        elif payload.quiz_type == 'fill_in_blanks':
            # Case-insensitive comparison
            is_correct = str(user_answer).lower().strip() == str(correct_answer).lower().strip()
            marks_awarded = q.get('marks', 1) if is_correct else 0
            
        elif payload.quiz_type == 'match_following':
            # Compare pairs
            user_pairs = user_answer if isinstance(user_answer, list) else [user_answer]
            correct_pairs = correct_answer if isinstance(correct_answer, list) else [correct_answer]
            is_correct = set(str(p) for p in user_pairs) == set(str(p) for p in correct_pairs)
            marks_awarded = q.get('marks', 5) if is_correct else 0
            
        elif payload.quiz_type == 'sentence_correction':
            # Case-insensitive, normalized comparison
            user_clean = str(user_answer).lower().strip()
            correct_clean = str(correct_answer).lower().strip()
            is_correct = user_clean == correct_clean
            marks_awarded = q.get('marks', 2) if is_correct else 0
            
        elif payload.quiz_type == 'short_answer':
            # Flexible matching - check if key terms are present
            user_ans_lower = str(user_answer).lower().strip()
            correct_ans_lower = str(correct_answer).lower().strip()
            is_correct = user_ans_lower == correct_ans_lower
            marks_awarded = q.get('marks', 2) if is_correct else 0
        
        score += marks_awarded
        detailed_results.append({
            'question_id': q_id,
            'user_answer': str(user_answer),
            'correct_answer': str(correct_answer),
            'is_correct': is_correct,
            'marks_awarded': marks_awarded
        })
    
    return score, total_marks, detailed_results


def update_lesson_progress(lesson_slug: str, user_email: str, score_percentage: float) -> Dict:
    """
    Update or create lesson progress document
    Returns updated progress document
    """
    progress_doc = db['lesson_progress'].find_one({
        'lesson_slug': lesson_slug,
        'user_email': user_email
    })
    
    if progress_doc:
        # Update existing progress
        attempts = progress_doc.get('attempts', 0) + 1
        scores = progress_doc.get('scores', [])
        scores.append(score_percentage)
        
        # Completed if score >= 70%
        completed = score_percentage >= 70 or progress_doc.get('completed', False)
        
        update_data = {
            'attempts': attempts,
            'scores': scores,
            'completed': completed,
            'latest_score': score_percentage,
            'latest_attempt_at': datetime.utcnow(),
            'avg_score': round(sum(scores) / len(scores), 2)
        }
        
        db['lesson_progress'].update_one(
            {'_id': progress_doc['_id']},
            {'$set': update_data}
        )
        
        progress_doc.update(update_data)
    else:
        # Create new progress
        progress_doc = {
            'lesson_slug': lesson_slug,
            'user_email': user_email,
            'attempts': 1,
            'scores': [score_percentage],
            'completed': score_percentage >= 70,
            'latest_score': score_percentage,
            'latest_attempt_at': datetime.utcnow(),
            'avg_score': score_percentage,
            'created_at': datetime.utcnow()
        }
        
        db['lesson_progress'].insert_one(progress_doc)
    
    return progress_doc


def get_student_metrics_for_ml(user_email: str) -> Dict:
    """
    Collect all necessary student metrics for ML model prediction
    """
    attempts = list(db['quiz_attempts'].find({'user_email': user_email}))
    progress = list(db['lesson_progress'].find({'user_email': user_email}))
    
    total_attempts = len(attempts)
    completed_lessons = len([p for p in progress if p.get('completed', False)])
    
    # Average score across all attempts
    avg_score = round(
        sum(a.get('quiz_score', 0) for a in attempts) / total_attempts, 2
    ) if total_attempts > 0 else 0.0
    
    # Completion rate
    total_lessons = db['lessons'].count_documents({})
    completion_rate = round(
        (completed_lessons / total_lessons) * 100, 2
    ) if total_lessons > 0 else 0.0
    
    # Average time per lesson
    times = [a.get('time_taken') for a in attempts if a.get('time_taken') is not None]
    avg_time_per_lesson = round(sum(times) / len(times), 2) if times else 0.0
    
    # Recent score trend (last 5 attempts)
    recent = sorted(attempts, key=lambda x: x.get('submitted_at', datetime.min), reverse=True)[:5]
    recent_scores = [a.get('quiz_score', 0) for a in recent]
    
    return {
        'avg_score': avg_score,
        'attempts': total_attempts,
        'completion_rate': completion_rate,
        'avg_time_per_lesson': avg_time_per_lesson,
        'recent_score_trend': sum(recent_scores) / len(recent_scores) if recent_scores else 0.0,
        'completed_lessons': completed_lessons
    }


def compute_student_metrics(user_email: str) -> Dict:
    """
    Backwards-compatible wrapper used by other modules.
    Returns the same structure as get_student_metrics_for_ml.
    """
    try:
        return get_student_metrics_for_ml(user_email)
    except Exception as e:
        # Fallback minimal metrics
        # print(f"Warning: compute_student_metrics fallback for {user_email}: {e}")
        logger.warning(f"compute_student_metrics fallback for {user_email}: {e}")
        return {
            'avg_score': 0.0,
            'attempts': 0,
            'completion_rate': 0.0,
            'avg_time_per_lesson': 0.0,
            'recent_score_trend': 0.0,
            'completed_lessons': 0
        }


# ===== Main Quiz Submission Endpoint =====

# @router.post('', response_model=Dict[str, Any])

@router.post("/", name="submit_quiz", response_model=Dict[str, Any])
async def submit_quiz(payload: QuizSubmissionPayload):
    """
    Submit quiz answers and get graded results with ML prediction.
    
    Flow:
    1. Validate lesson and quiz exist
    2. Grade the quiz based on quiz type
    3. Calculate score as percentage
    4. Update lesson progress and attempts
    5. Get ML prediction for learning path
    6. Store attempt in database
    7. Return detailed results
    """
    
    # 1. Validate lesson exists
    lesson = db['lessons'].find_one({'slug': payload.lesson_slug})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # 2. Validate quiz exists
    quiz_doc = db['quizzes'].find_one({'lesson_slug': payload.lesson_slug})
    if not quiz_doc:
        raise HTTPException(status_code=404, detail="Quiz not found for this lesson")
    
    # 3. Grade the quiz
    try:
        score_earned, total_marks, detailed_results = calculate_score(payload, quiz_doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Grading error: {str(e)}")
    
    # 4. Calculate percentage and check if passed
    quiz_percentage = round((score_earned / total_marks * 100), 2) if total_marks > 0 else 0
    passed = quiz_percentage >= 70
    
    # 5. Update lesson progress
    progress_doc = update_lesson_progress(payload.lesson_slug, payload.user_email, quiz_percentage)
    attempt_number = progress_doc.get('attempts', 1)
    lesson_completed = progress_doc.get('completed', False)
    
    # 6. Record attempt in database
    attempt_record = {
        'lesson_slug': payload.lesson_slug,
        'user_email': payload.user_email,
        'quiz_type': payload.quiz_type,
        'score_earned': score_earned,
        'total_marks': total_marks,
        'quiz_score': quiz_percentage,
        'passed': passed,
        'attempt_number': attempt_number,
        'detailed_results': detailed_results,
        'time_taken': payload.time_taken,
        'submitted_at': datetime.utcnow()
    }
    
    try:
        db['quiz_attempts'].insert_one(attempt_record)
    except Exception as e:
        logger.warning(f"Failed to save attempt: {e}")
        
    
    # 7. Update user learning path using ML model
    from ..services.student_metrics import update_user_learning_path, get_user_metrics
    try:
        update_user_learning_path(payload.user_email)
        ml_prediction = get_user_metrics(payload.user_email)
    except Exception as e:
        logger.warning(f"ML prediction failed: {e}")
        ml_prediction = {
            'predicted_level': 'Beginner',
            'confidence': 0,
            'difficulty_adjustment': 'Maintain',
            'recommended_lessons': []
        }

    # 8. Return comprehensive response
    response = {
        'lesson_slug': payload.lesson_slug,
        'lesson_title': lesson.get('title'),
        'quiz_type': payload.quiz_type,
        'score_earned': score_earned,
        'total_marks': total_marks,
        'percentage': quiz_percentage,
        'passed': passed,
        'attempt_number': attempt_number,
        'lesson_completed': lesson_completed,
        'detailed_results': detailed_results,
        'ml_prediction': ml_prediction
    }

    return response



