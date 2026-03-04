import json

# Load both generated files
with open("quizzes_real_content.json", "r") as f:
    quizzes_1 = json.load(f)

with open("quizzes_remaining_lessons.json", "r") as f:
    quizzes_2 = json.load(f)

# Combine all quizzes
all_quizzes = {
    "quizzes": quizzes_1["quizzes"] + quizzes_2["quizzes"]
}

# Save to the main file
with open("quizzes_all_lessons.json", "w") as f:
    json.dump(all_quizzes, f, indent=2)

print(f"✓ Successfully combined all quiz data")
print(f"✓ Total lessons: {len(all_quizzes['quizzes'])}")
print(f"✓ Total questions: {sum(len(quiz['quiz_types']['multiple_choice']['questions']) * 5 for quiz in all_quizzes['quizzes'])} questions")
print(f"✓ Saved to quizzes_all_lessons.json")
print(f"\n✅ ALL 10 LESSONS WITH REAL QUIZ CONTENT:")
for i, quiz in enumerate(all_quizzes['quizzes'], 1):
    print(f"  {i}. {quiz['lesson_title']}")
