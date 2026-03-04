import os
import pickle
from datetime import datetime
from typing import Dict, Any

from app.db import db

_MODEL = None

def load_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'models', 'student_level_model.pkl')
    # Fallback path
    alt = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..', 'backend', 'models', 'student_level_model.pkl')
    if os.path.exists(model_path):
        path = model_path
    elif os.path.exists(alt):
        path = alt
    else:
        path = None

    if path:
        try:
            with open(path, 'rb') as f:
                _MODEL = pickle.load(f)
        except Exception:
            _MODEL = None
    else:
        _MODEL = None

    return _MODEL


def get_user_metrics(user_email: str) -> Dict[str, Any]:
    """
    Compute student metrics from quiz_attempts collection and use ML model to predict level.
    Returns a dict with metrics and prediction.
    """
    attempts = list(db['quiz_attempts'].find({'user_email': user_email}))

    total_attempts = len(attempts)
    lessons_attempted = len(set(a.get('lesson_slug') for a in attempts))
    # average percentage score
    avg_score = round(sum(a.get('quiz_score', 0) for a in attempts) / total_attempts, 2) if total_attempts > 0 else 0.0
    # completion rate: lessons attempted / total lessons in DB
    total_lessons = db['lessons'].count_documents({})
    completion_rate = round((lessons_attempted / total_lessons) * 100, 2) if total_lessons > 0 else 0.0
    # average time per lesson if provided
    times = [a.get('time_taken') for a in attempts if a.get('time_taken') is not None]
    avg_time = round(sum(times) / len(times), 2) if len(times) > 0 else 0.0

    # recent score trend (last 5)
    recent = sorted(attempts, key=lambda x: x.get('submitted_at', datetime.min), reverse=True)[:5]
    recent_scores = [a.get('quiz_score', 0) for a in recent]

    metrics = {
        'total_attempts': total_attempts,
        'lessons_attempted': lessons_attempted,
        'avg_score': avg_score,
        'completion_rate': completion_rate,
        'avg_time_per_lesson': avg_time,
        'recent_score_trend': recent_scores
    }

    # Default prediction
    predicted_level = 'Beginner'
    confidence = 0.0
    difficulty_adjustment = 0.0
    recommended_lessons = []

    model = load_model()
    if model is not None:
        try:
            # Build simple feature vector: [avg_score, total_attempts, completion_rate, avg_time]
            features = [[metrics['avg_score'], metrics['total_attempts'], metrics['completion_rate'], metrics['avg_time_per_lesson']]]
            # Try predict_proba if available
            if hasattr(model, 'predict_proba'):
                probs = model.predict_proba(features)[0]
                # choose class with highest prob
                classes = list(getattr(model, 'classes_', []))
                if classes and len(probs) == len(classes):
                    try:
                        idx = int(probs.argmax())
                    except Exception:
                        idx = probs.index(max(probs))
                    predicted_level = classes[idx]
                    confidence = float(max(probs))
                else:
                    predicted_level = str(model.predict(features)[0])
                    confidence = 0.5
            else:
                predicted_level = str(model.predict(features)[0])
                confidence = 0.5
        except Exception:
            predicted_level = 'Beginner'
            confidence = 0.0

    # Recommend lessons with lowest average scores
    lesson_scores = {}
    for a in attempts:
        l = a.get('lesson_slug')
        lesson_scores.setdefault(l, []).append(a.get('quiz_score', 0))

    avg_per_lesson = [(l, round(sum(scores)/len(scores),2)) for l, scores in lesson_scores.items()]
    avg_per_lesson.sort(key=lambda x: x[1])
    recommended_lessons = [l for l, s in avg_per_lesson[:5]]

    # difficulty_adjustment: suggest increasing difficulty if avg_score > 80
    if metrics['avg_score'] >= 85:
        difficulty_adjustment = 1  # increase
    elif metrics['avg_score'] < 50:
        difficulty_adjustment = -1  # decrease
    else:
        difficulty_adjustment = 0

    return {
        'metrics': metrics,
        'predicted_level': predicted_level,
        'confidence': confidence,
        'difficulty_adjustment': difficulty_adjustment,
        'recommended_lessons': recommended_lessons
    }
from datetime import datetime, timedelta
from app.db import db
from app.ml.level_predictor import predict_learning_path

def compute_student_metrics(email: str):
    """
    Computes metrics required by ML model from user quiz attempts.
    Returns metrics dict with: avg_score, attempts, completion_rate, avg_time_per_lesson, recent_score_trend
    """
    
    quiz_attempts = list(db['quiz_attempts'].find({'user_email': email}))
    
    if not quiz_attempts:
        return {
            "avg_score": 0.0,
            "attempts": 0,
            "completion_rate": 0.0,
            "avg_time_per_lesson": 0.0,
            "recent_score_trend": 0.0
        }
    
    total = len(quiz_attempts)
    
    # Calculate average score (extract from quiz_score field)
    scores = [float(a.get('quiz_score', 0)) for a in quiz_attempts]
    avg_score = sum(scores) / total if total > 0 else 0.0
    
    # Completion rate (all quiz attempts count as 1.0 each if submitted)
    completion_rate = 1.0  # Since these are submitted attempts
    
    # Average time per lesson (if time_spent is tracked)
    times = [float(a.get('time_spent', 0)) for a in quiz_attempts if a.get('time_spent')]
    avg_time_per_lesson = sum(times) / len(times) if times else 0.0
    
    # Recent score trend: compare last 5 attempts vs older attempts
    sorted_attempts = sorted(quiz_attempts, key=lambda x: x.get('submitted_at', datetime.utcnow()))
    
    recent = sorted_attempts[-5:]
    previous = sorted_attempts[:-5]
    
    recent_scores = [float(a.get('quiz_score', 0)) for a in recent]
    recent_avg = sum(recent_scores) / len(recent_scores) if recent_scores else avg_score
    
    if previous:
        prev_scores = [float(a.get('quiz_score', 0)) for a in previous]
        prev_avg = sum(prev_scores) / len(prev_scores)
        recent_score_trend = recent_avg - prev_avg
    else:
        recent_score_trend = 0.0
    
    return {
        "avg_score": round(avg_score, 2),
        "attempts": total,
        "completion_rate": round(completion_rate, 2),
        "avg_time_per_lesson": round(avg_time_per_lesson, 2),
        "recent_score_trend": round(recent_score_trend, 2)
    }


def update_user_learning_path(email: str):
    """
    Compute student metrics and update user's predicted level using ML model.
    Call this after each quiz submission.
    """
    
    metrics = compute_student_metrics(email)
    
    # Skip if no attempts yet
    if metrics['attempts'] == 0:
        return
    
    # Call ML model to get prediction
    try:
        prediction = predict_learning_path(metrics)
        
        # Update user document with prediction results
        db['users'].update_one(
            {'email': email},
            {
                '$set': {
                    'predicted_level': prediction['predicted_level'],
                    'confidence': prediction['confidence'],
                    'difficulty_adjustment': prediction['difficulty_adjustment'],
                    'recommended_lessons': prediction['recommended_lessons'],
                    'last_updated': datetime.utcnow()
                }
            }
        )
    except Exception as e:
        print(f"Error updating learning path for {email}: {str(e)}")


def get_user_metrics(email: str):
    """Get current metrics and prediction for a user."""
    metrics = compute_student_metrics(email)
    user_doc = db['users'].find_one({'email': email})
    
    return {
        'metrics': metrics,
        'predicted_level': user_doc.get('predicted_level', 'Beginner') if user_doc else 'Beginner',
        'confidence': user_doc.get('confidence', 0.0) if user_doc else 0.0,
        'difficulty_adjustment': user_doc.get('difficulty_adjustment', 'Maintain') if user_doc else 'Maintain',
        'recommended_lessons': user_doc.get('recommended_lessons', []) if user_doc else []
    }


from app.db import db
from datetime import datetime
import traceback

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    from bson import ObjectId
    if not doc:
        return {}
    if isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, dict):
        return {k: serialize_doc(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_doc(i) for i in doc]
    return doc

def get_user_progress(user_email: str):
    results = list(db['exercise_results'].find({'user_email': user_email}))
    results = [serialize_doc(r) for r in results]

    total = len(results)
    avg_score = sum(r.get('evaluation', {}).get('score', 0) for r in results)/total if total > 0 else 0

    recent = results[-10:] if total > 0 else []
    return {
        'count': total,
        'avg_score': avg_score,
        'recent': recent
    }

def predict_learning_path(results, level="beginner"):
    """
    Generate a personalized learning path based on user's exercise results.
    """
    if not results:
        return ["Start with beginner lessons"]

    weak_lessons = [r['lesson_id'] for r in results if r.get('evaluation', {}).get('score', 1) < 0.75]
    weak_lessons = list(set(weak_lessons))

    if not weak_lessons:
        return ["Advance to next level lessons"]

    return [f"Review lesson {lesson_id}" for lesson_id in weak_lessons]

def update_user_learning_path(user_email: str):
    try:
        results = list(db['exercise_results'].find({'user_email': user_email}))
        path = predict_learning_path(results)
        db['users'].update_one({'email': user_email}, {'$set': {'recommended_path': path}})
        return path
    except Exception as e:
        traceback.print_exc()
        return ["Error computing learning path"]
