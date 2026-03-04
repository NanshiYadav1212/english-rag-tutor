from app.ml.level_predictor import predict_learning_path
sample_student = {
    "avg_score": 0.85,
    "attempts": 12,
    "completion_rate": 0.9,
    "avg_time_per_lesson": 10.5,
    "recent_score_trend": 0.1
}

result = predict_learning_path(sample_student)
print(result)
