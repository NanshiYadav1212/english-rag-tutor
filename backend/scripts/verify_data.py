from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['english_tutor']

# Check a lesson
lesson = db['lessons'].find_one({'slug': 'basics-of-english-grammar'})
if lesson:
    examples = lesson.get('examples', [])
    title = lesson['title']
    print(f'✓ Lesson: {title}')
    print(f'  - Practical Examples: {len(examples)} examples')
    if examples:
        ex = examples[0]
        print(f'  - First example keys: {list(ex.keys())}')
        q = ex.get("question", "?")
        print(f'  - Question: {q[:60]}...' if len(q) > 60 else f'  - Question: {q}')
    
    print()

# Check all lessons have 3 examples
print("Checking all lessons for practical examples:")
all_lessons = list(db['lessons'].find())
for lesson in all_lessons:
    examples = lesson.get('examples', [])
    title = lesson['title']
    print(f'  {title}: {len(examples)} examples')

print()

# Check a quiz
quiz = db['quizzes'].find_one({'lesson_slug': 'basics-of-english-grammar'})
if quiz:
    lesson_title = quiz['lesson_title']
    print(f'✓ Quiz for: {lesson_title}')
    total_q = 0
    for qtype, qdata in quiz.get('quiz_types', {}).items():
        count = len(qdata.get('questions', []))
        total_q += count
        qtype_name = qdata.get('type', qtype)
        print(f'  - {qtype_name}: {count} questions')
    print(f'  - Total: {total_q} questions')

print()
print("All 10 lessons should have:")
print("  ✓ 3 practical examples each")
print("  ✓ 50 quiz questions each (5 types × 10 questions)")
