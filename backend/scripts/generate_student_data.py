import numpy as np
import pandas as pd

np.random.seed(42)

data = []

for _ in range(600):
    avg_score = np.random.uniform(0.2, 0.95)
    attempts = np.random.randint(5, 40)
    completion_rate = np.random.uniform(0.3, 1.0)
    avg_time = np.random.uniform(5, 25)
    trend = np.random.uniform(-0.3, 0.3)

    # Label logic
    if avg_score < 0.5 and completion_rate < 0.6:
        level = 0  # Beginner
    elif avg_score > 0.8 and completion_rate > 0.85 and trend > 0:
        level = 2  # Advanced
    else:
        level = 1  # Intermediate

    data.append([
        avg_score,
        attempts,
        completion_rate,
        avg_time,
        trend,
        level
    ])

columns = [
    "avg_score",
    "attempts",
    "completion_rate",
    "avg_time_per_lesson",
    "recent_score_trend",
    "level"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("models/student_level_data.csv", index=False)

print("Dataset created:", df.shape)
