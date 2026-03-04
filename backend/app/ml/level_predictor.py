import joblib
import numpy as np

MODEL_PATH = "models/student_level_model.pkl"

# Load model once at startup
model = joblib.load(MODEL_PATH)

LEVEL_MAP = {
    0: "Beginner",
    1: "Intermediate",
    2: "Advanced"
}

def predict_learning_path(student_metrics: dict):
    """
    student_metrics keys:
    - avg_score
    - attempts
    - completion_rate
    - avg_time_per_lesson
    - recent_score_trend
    """

    features = np.array([[
        student_metrics["avg_score"],
        student_metrics["attempts"],
        student_metrics["completion_rate"],
        student_metrics["avg_time_per_lesson"],
        student_metrics["recent_score_trend"]
    ]])

    level_idx = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    return {
        "predicted_level": LEVEL_MAP[level_idx],
        "confidence": round(float(max(probabilities)), 2),
        "difficulty_adjustment": _difficulty_action(level_idx),
        "recommended_lessons": _lesson_recommendation(level_idx)
    }

def _difficulty_action(level_idx: int):
    if level_idx == 0:
        return "Decrease"
    elif level_idx == 2:
        return "Increase"
    return "Maintain"

def _lesson_recommendation(level_idx: int):
    if level_idx == 0:
        return ["Foundation Review", "Basic Practice"]
    elif level_idx == 2:
        return ["Advanced Challenges", "Real-world Projects"]
    return ["Current Level Practice"]
