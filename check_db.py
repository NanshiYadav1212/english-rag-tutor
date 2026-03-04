import os
from pymongo import MongoClient

# Check what database name is being used
mongo_db = os.getenv("MONGO_DB", "tutor_db")
print(f"Database name being used: {mongo_db}")

# Check what's actually in MongoDB
client = MongoClient('mongodb://localhost:27017/')

print("\nDatabases available:")
for db_name in client.list_database_names():
    print(f"  - {db_name}")

# Check both databases
for db_name in ["tutor_db", "english_tutor"]:
    db = client[db_name]
    lesson_count = db['lessons'].count_documents({})
    quiz_count = db['quizzes'].count_documents({})
    print(f"\nDatabase '{db_name}':")
    print(f"  Lessons: {lesson_count}")
    print(f"  Quizzes: {quiz_count}")
    
    if lesson_count > 0:
        first_lesson = db['lessons'].find_one()
        print(f"  First lesson: {first_lesson['title']}")
        print(f"  Examples: {len(first_lesson.get('examples', []))}")
