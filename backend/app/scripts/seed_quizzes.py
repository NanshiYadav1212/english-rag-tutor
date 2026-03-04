"""
Seed script to populate quiz questions for all 10 lessons.
Each lesson has 5 quiz types with 10 questions each.
Run from backend: python -m app.scripts.seed_quizzes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db import db
from datetime import datetime

QUIZZES_DATA = {
    "past-simple-tense": {
        "multiple_choice": {
            "total_marks": 10,
            "questions": [
                {
                    "question_id": "mc1",
                    "quiz_type": "multiple_choice",
                    "question_text": "What is the past simple form of 'go'?",
                    "options": ["go", "went", "gone", "going"],
                    "correct_answer": "went",
                    "marks": 1
                },
                {
                    "question_id": "mc2",
                    "quiz_type": "multiple_choice",
                    "question_text": "Choose the correct sentence:",
                    "options": ["She go to school yesterday", "She went to school yesterday", "She goes to school yesterday", "She going to school yesterday"],
                    "correct_answer": "She went to school yesterday",
                    "marks": 1
                },
                {
                    "question_id": "mc3",
                    "quiz_type": "multiple_choice",
                    "question_text": "I ___ a movie last night.",
                    "options": ["watch", "watched", "am watching", "have watched"],
                    "correct_answer": "watched",
                    "marks": 1
                },
                {
                    "question_id": "mc4",
                    "quiz_type": "multiple_choice",
                    "question_text": "Did he ___ to the party?",
                    "options": ["come", "came", "coming", "comes"],
                    "correct_answer": "come",
                    "marks": 1
                },
                {
                    "question_id": "mc5",
                    "quiz_type": "multiple_choice",
                    "question_text": "They ___ in Paris for two weeks.",
                    "options": ["stay", "stayed", "are staying", "have stayed"],
                    "correct_answer": "stayed",
                    "marks": 1
                },
                {
                    "question_id": "mc6",
                    "quiz_type": "multiple_choice",
                    "question_text": "She ___ breakfast before work.",
                    "options": ["eat", "eats", "ate", "eaten"],
                    "correct_answer": "ate",
                    "marks": 1
                },
                {
                    "question_id": "mc7",
                    "quiz_type": "multiple_choice",
                    "question_text": "We ___ friends in college.",
                    "options": ["become", "became", "becoming", "becomes"],
                    "correct_answer": "became",
                    "marks": 1
                },
                {
                    "question_id": "mc8",
                    "quiz_type": "multiple_choice",
                    "question_text": "When ___ you arrive?",
                    "options": ["did", "do", "does", "will"],
                    "correct_answer": "did",
                    "marks": 1
                },
                {
                    "question_id": "mc9",
                    "quiz_type": "multiple_choice",
                    "question_text": "I ___ not see him yesterday.",
                    "options": ["did", "do", "am", "have"],
                    "correct_answer": "did",
                    "marks": 1
                },
                {
                    "question_id": "mc10",
                    "quiz_type": "multiple_choice",
                    "question_text": "The conference ___ last month.",
                    "options": ["happens", "happened", "is happening", "has happened"],
                    "correct_answer": "happened",
                    "marks": 1
                }
            ]
        },
        "fill_blank": {
            "total_marks": 10,
            "questions": [
                {
                    "question_id": "fb1",
                    "quiz_type": "fill_blank",
                    "sentence": "He ___ to the market yesterday.",
                    "correct_answer": "went",
                    "marks": 1
                },
                {
                    "question_id": "fb2",
                    "quiz_type": "fill_blank",
                    "sentence": "She ___ a beautiful dress last week.",
                    "correct_answer": "bought",
                    "marks": 1
                },
                {
                    "question_id": "fb3",
                    "quiz_type": "fill_blank",
                    "sentence": "They ___ the movie at the cinema.",
                    "correct_answer": "watched",
                    "marks": 1
                },
                {
                    "question_id": "fb4",
                    "quiz_type": "fill_blank",
                    "sentence": "I ___ breakfast at 7 AM.",
                    "correct_answer": "had",
                    "marks": 1
                },
                {
                    "question_id": "fb5",
                    "quiz_type": "fill_blank",
                    "sentence": "We ___ in London for five years.",
                    "correct_answer": "lived",
                    "marks": 1
                },
                {
                    "question_id": "fb6",
                    "quiz_type": "fill_blank",
                    "sentence": "You ___ your homework yesterday?",
                    "correct_answer": "did",
                    "marks": 1
                },
                {
                    "question_id": "fb7",
                    "quiz_type": "fill_blank",
                    "sentence": "The children ___ in the park.",
                    "correct_answer": "played",
                    "marks": 1
                },
                {
                    "question_id": "fb8",
                    "quiz_type": "fill_blank",
                    "sentence": "He ___ the letter yesterday morning.",
                    "correct_answer": "wrote",
                    "marks": 1
                },
                {
                    "question_id": "fb9",
                    "quiz_type": "fill_blank",
                    "sentence": "She ___ not like the restaurant.",
                    "correct_answer": "did",
                    "marks": 1
                },
                {
                    "question_id": "fb10",
                    "quiz_type": "fill_blank",
                    "sentence": "We ___ the meeting at noon.",
                    "correct_answer": "attended",
                    "marks": 1
                }
            ]
        },
        "true_false": {
            "total_marks": 10,
            "questions": [
                {
                    "question_id": "tf1",
                    "quiz_type": "true_false",
                    "statement": "Past simple is used for actions completed in the past.",
                    "correct_answer": True,
                    "marks": 1
                },
                {
                    "question_id": "tf2",
                    "quiz_type": "true_false",
                    "statement": "All past simple verbs end in -ed.",
                    "correct_answer": False,
                    "marks": 1
                },
                {
                    "question_id": "tf3",
                    "quiz_type": "true_false",
                    "statement": "'Did' is used with regular verbs only.",
                    "correct_answer": False,
                    "marks": 1
                },
                {
                    "question_id": "tf4",
                    "quiz_type": "true_false",
                    "statement": "Irregular verbs have unique past forms.",
                    "correct_answer": True,
                    "marks": 1
                },
                {
                    "question_id": "tf5",
                    "quiz_type": "true_false",
                    "statement": "The sentence 'I went home' is correct.",
                    "correct_answer": True,
                    "marks": 1
                },
                {
                    "question_id": "tf6",
                    "quiz_type": "true_false",
                    "statement": "'He was going' is past simple tense.",
                    "correct_answer": False,
                    "marks": 1
                },
                {
                    "question_id": "tf7",
                    "quiz_type": "true_false",
                    "statement": "Questions in past simple invert subject and auxiliary.",
                    "correct_answer": True,
                    "marks": 1
                },
                {
                    "question_id": "tf8",
                    "quiz_type": "true_false",
                    "statement": "'She bought' is an irregular past simple form.",
                    "correct_answer": False,
                    "marks": 1
                },
                {
                    "question_id": "tf9",
                    "quiz_type": "true_false",
                    "statement": "Past simple is often used for stories.",
                    "correct_answer": True,
                    "marks": 1
                },
                {
                    "question_id": "tf10",
                    "quiz_type": "true_false",
                    "statement": "'Did you see?' is a valid negative question.",
                    "correct_answer": False,
                    "marks": 1
                }
            ]
        },
        "match": {
            "total_marks": 15,
            "questions": [
                {
                    "question_id": "m1",
                    "quiz_type": "match",
                    "question_text": "Match the verbs with their past forms:",
                    "left_items": ["go", "eat", "see", "take", "write", "buy"],
                    "right_items": ["wrote", "went", "bought", "took", "saw", "ate"],
                    "correct_pairs": [
                        {"left": "go", "right": "went"},
                        {"left": "eat", "right": "ate"},
                        {"left": "see", "right": "saw"},
                        {"left": "take", "right": "took"},
                        {"left": "write", "right": "wrote"},
                        {"left": "buy", "right": "bought"}
                    ],
                    "marks": 6
                },
                {
                    "question_id": "m2",
                    "quiz_type": "match",
                    "question_text": "Match sentences with their past simple forms:",
                    "left_items": ["He runs", "She goes", "They eat", "I play", "You work"],
                    "right_items": ["I played", "He ran", "She went", "You worked", "They ate"],
                    "correct_pairs": [
                        {"left": "He runs", "right": "He ran"},
                        {"left": "She goes", "right": "She went"},
                        {"left": "They eat", "right": "They ate"},
                        {"left": "I play", "right": "I played"},
                        {"left": "You work", "right": "You worked"}
                    ],
                    "marks": 5
                },
                {
                    "question_id": "m3",
                    "quiz_type": "match",
                    "question_text": "Match time expressions with tenses:",
                    "left_items": ["last week", "yesterday", "in 2020", "last month", "ago"],
                    "right_items": ["past", "past", "past", "past", "past"],
                    "correct_pairs": [
                        {"left": "last week", "right": "past"},
                        {"left": "yesterday", "right": "past"},
                        {"left": "in 2020", "right": "past"},
                        {"left": "last month", "right": "past"},
                        {"left": "ago", "right": "past"}
                    ],
                    "marks": 5
                }
            ]
        },
        "short_answer": {
            "total_marks": 10,
            "questions": [
                {
                    "question_id": "sa1",
                    "quiz_type": "short_answer",
                    "question_text": "Write the past simple of 'go':",
                    "acceptable_answers": ["went"],
                    "marks": 1
                },
                {
                    "question_id": "sa2",
                    "quiz_type": "short_answer",
                    "question_text": "Provide the past form of 'have':",
                    "acceptable_answers": ["had"],
                    "marks": 1
                },
                {
                    "question_id": "sa3",
                    "quiz_type": "short_answer",
                    "question_text": "What auxiliary do we use for questions in past simple?",
                    "acceptable_answers": ["did", "Did"],
                    "marks": 1
                },
                {
                    "question_id": "sa4",
                    "quiz_type": "short_answer",
                    "question_text": "Convert 'I am' to past simple:",
                    "acceptable_answers": ["i was", "I was", "was"],
                    "marks": 1
                },
                {
                    "question_id": "sa5",
                    "quiz_type": "short_answer",
                    "question_text": "Describe a time reference commonly used with past simple:",
                    "acceptable_answers": ["yesterday", "last week", "last year", "in 2020", "long ago", "ages ago"],
                    "marks": 2
                },
                {
                    "question_id": "sa6",
                    "quiz_type": "short_answer",
                    "question_text": "What is the past simple form of 'do'?",
                    "acceptable_answers": ["did"],
                    "marks": 1
                },
                {
                    "question_id": "sa7",
                    "quiz_type": "short_answer",
                    "question_text": "Is 'watched' a regular or irregular verb?",
                    "acceptable_answers": ["regular"],
                    "marks": 1
                },
                {
                    "question_id": "sa8",
                    "quiz_type": "short_answer",
                    "question_text": "Write a negative past simple sentence with 'like':",
                    "acceptable_answers": ["i didn't like", "I didn't like", "he didn't like", "she didn't like", "they didn't like"],
                    "marks": 1
                },
                {
                    "question_id": "sa9",
                    "quiz_type": "short_answer",
                    "question_text": "What is the past form of 'see'?",
                    "acceptable_answers": ["saw"],
                    "marks": 1
                },
                {
                    "question_id": "sa10",
                    "quiz_type": "short_answer",
                    "question_text": "How many verb forms exist for most regular verbs in English?",
                    "acceptable_answers": ["4", "four"],
                    "marks": 1
                }
            ]
        }
    }
}


def seed_all_quizzes():
    """Seed quiz questions for all lessons."""
    
    # Get all lessons
    lessons = list(db['lessons'].find({}))
    
    if not lessons:
        print("No lessons found. Please run init_db first.")
        return
    
    print(f"Found {len(lessons)} lessons. Seeding quizzes...")
    
    for lesson in lessons:
        lesson_slug = lesson['slug']
        lesson_title = lesson['title']
        
        # For now, we'll create the structure for all lessons with a template
        # In production, you'd customize each quiz
        
        for quiz_type in ['multiple_choice', 'fill_blank', 'true_false', 'match', 'short_answer']:
            quiz_doc = db['quiz_questions'].find_one({
                'lesson_slug': lesson_slug,
                'quiz_type': quiz_type
            })
            
            if quiz_doc:
                print(f"  {lesson_title} - {quiz_type}: Already exists")
                continue
            
            # Use template from first lesson or create generic
            if lesson_slug in QUIZZES_DATA and quiz_type in QUIZZES_DATA[lesson_slug]:
                quiz_data = QUIZZES_DATA[lesson_slug][quiz_type]
            else:
                # Generic template for other lessons
                quiz_data = create_generic_quiz(lesson_title, quiz_type)
            
            db['quiz_questions'].insert_one({
                'lesson_slug': lesson_slug,
                'lesson_title': lesson_title,
                'quiz_type': quiz_type,
                'total_marks': quiz_data['total_marks'],
                'questions': quiz_data['questions'],
                'created_at': datetime.utcnow()
            })
            
            print(f"  ✓ {lesson_title} - {quiz_type}: {len(quiz_data['questions'])} questions")
    
    print("\nQuiz seeding complete!")


def create_generic_quiz(lesson_title: str, quiz_type: str):
    """Create generic quiz template for lessons without specific data."""
    
    if quiz_type == 'multiple_choice':
        return {
            'total_marks': 10,
            'questions': [
                {
                    'question_id': f'mc{i}',
                    'quiz_type': 'multiple_choice',
                    'question_text': f'Sample question {i} from {lesson_title}?',
                    'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                    'correct_answer': 'Option A',
                    'marks': 1
                }
                for i in range(1, 11)
            ]
        }
    elif quiz_type == 'fill_blank':
        return {
            'total_marks': 10,
            'questions': [
                {
                    'question_id': f'fb{i}',
                    'quiz_type': 'fill_blank',
                    'sentence': f'This is a sample sentence for {lesson_title} with a blank: ___.',
                    'correct_answer': 'answer',
                    'marks': 1
                }
                for i in range(1, 11)
            ]
        }
    elif quiz_type == 'true_false':
        return {
            'total_marks': 10,
            'questions': [
                {
                    'question_id': f'tf{i}',
                    'quiz_type': 'true_false',
                    'statement': f'This is a sample statement about {lesson_title}.',
                    'correct_answer': i % 2 == 0,
                    'marks': 1
                }
                for i in range(1, 11)
            ]
        }
    elif quiz_type == 'match':
        return {
            'total_marks': 15,
            'questions': [
                {
                    'question_id': 'm1',
                    'quiz_type': 'match',
                    'question_text': f'Match items from {lesson_title}:',
                    'left_items': ['Item 1', 'Item 2', 'Item 3'],
                    'right_items': ['Definition 1', 'Definition 2', 'Definition 3'],
                    'correct_pairs': [
                        {'left': 'Item 1', 'right': 'Definition 1'},
                        {'left': 'Item 2', 'right': 'Definition 2'},
                        {'left': 'Item 3', 'right': 'Definition 3'}
                    ],
                    'marks': 3
                }
            ]
        }
    else:  # short_answer
        return {
            'total_marks': 10,
            'questions': [
                {
                    'question_id': f'sa{i}',
                    'quiz_type': 'short_answer',
                    'question_text': f'Sample short answer question {i} about {lesson_title}?',
                    'acceptable_answers': ['answer', 'possible answer'],
                    'marks': 1
                }
                for i in range(1, 11)
            ]
        }


if __name__ == '__main__':
    seed_all_quizzes()
