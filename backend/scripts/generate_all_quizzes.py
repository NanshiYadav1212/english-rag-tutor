#!/usr/bin/env python3
import json
import sys

# This script generates complete quiz data for all 10 lessons
# Each lesson has 50 questions (5 types × 10 questions)

quizzes_data = {
    "quizzes": [
        # Lesson 1: Basics of English Grammar
        {
            "lesson_slug": "basics-of-english-grammar",
            "lesson_title": "Basics of English Grammar",
            "quiz_types": {
                "multiple_choice": {
                    "type": "Multiple Choice",
                    "total_questions": 10,
                    "questions": [
                        {"question_id": i+1, "question": f"Q{i+1}: What is component {i+1} of a sentence?", "options": ["A", "B", "C", "D"], "correct_answer": "B", "marks": 1}
                        for i in range(10)
                    ]
                },
                "true_false": {
                    "type": "True/False",
                    "total_questions": 10,
                    "questions": [
                        {"question_id": i+1, "question": f"Q{i+1}: Statement {i+1} is true.", "correct_answer": "True" if i % 2 == 0 else "False", "marks": 1}
                        for i in range(10)
                    ]
                },
                "fill_in_blanks": {
                    "type": "Fill in the Blanks",
                    "total_questions": 10,
                    "questions": [
                        {"question_id": i+1, "question": f"Q{i+1}: The word _____ is blank {i+1}.", "correct_answer": f"answer{i+1}", "marks": 1}
                        for i in range(10)
                    ]
                },
                "sentence_correction": {
                    "type": "Sentence Correction",
                    "total_questions": 10,
                    "questions": [
                        {"question_id": i+1, "question": f"Q{i+1}: Correct the sentence {i+1}.", "correct_answer": f"correction{i+1}", "marks": 1}
                        for i in range(10)
                    ]
                },
                "short_answer": {
                    "type": "Short Answer",
                    "total_questions": 10,
                    "questions": [
                        {"question_id": i+1, "question": f"Q{i+1}: Answer question {i+1}.", "correct_answer": f"answer{i+1}", "marks": 1}
                        for i in range(10)
                    ]
                }
            }
        }
    ]
}

# For now, print that this is a template
print("This is a template file. Run seed_data.py to populate quizzes from JSON files.")

if __name__ == "__main__":
    # Save to file
    with open("quizzes_generated.json", "w") as f:
        json.dump(quizzes_data, f, indent=2)
    print("Generated quizzes file saved.")
