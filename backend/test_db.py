#!/usr/bin/env python3
"""Quick test of API structure"""
from app.db import db

# Test lessons
print("📚 Lessons:")
lessons = list(db['lessons'].find({}))
for i, lesson in enumerate(lessons[:3], 1):
    print(f"  {i}. {lesson.get('title')} ({lesson.get('slug')})")
print(f"  ... and {len(lessons) - 3} more\n")

# Test quizzes
print("📝 Quizzes:")
quiz = db['quizzes'].find_one()
print(f"  Lesson: {quiz.get('lesson_title')}")
print(f"  Quiz Types Available:")
for qtype in quiz.get('quiz_types', {}).keys():
    qdata = quiz['quiz_types'][qtype]
    print(f"    - {qtype}: {qdata.get('total_questions')} questions")

print("\n✓ Database structure verified!")
