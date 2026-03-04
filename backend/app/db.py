# # import os
# # from pymongo import MongoClient
# # from dotenv import load_dotenv

# # load_dotenv()
# # MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
# # DB_NAME = os.getenv("MONGO_DB", "tutor_db")
# # client = MongoClient(MONGO_URL)
# # db = client[DB_NAME]

# # def init_db():
# #     lessons = db['lessons']
# #     users = db['users']
# #     lessons.create_index('slug', unique=True)
# #     users.create_index('email', unique=True)
# #     if lessons.count_documents({}) == 0:
# #         sample = [
# #             {
# #                 'title': 'Past Simple Basics',
# #                 'slug': 'past-simple-1',
# #                 'description': 'Practice past simple tense.',
# #                 'content': {'exercises': [
# #                     {'id': 'ps-1', 'prompt': 'He _ to the market yesterday.', 'answer': 'went'}
# #                 ]}
# #             },
# #             {
# #                 'title': 'Subject-Verb Agreement',
# #                 'slug': 'sv-agree-1',
# #                 'description': 'Match verbs to subjects.',
# #                 'content': {'exercises': [
# #                     {'id': 'sv-1', 'prompt': 'She (go) to school every day.', 'answer': 'goes'}
# #                 ]}
# #             }
# #         ]
# #         lessons.insert_many(sample)


# import os
# from pymongo import MongoClient
# from dotenv import load_dotenv

# load_dotenv()

# MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
# DB_NAME = os.getenv("MONGO_DB", "tutor_db")

# client = MongoClient(MONGO_URL)
# db = client[DB_NAME]

# def init_db():
#     lessons = db['lessons']
#     users = db['users']
#     lessons.create_index('slug', unique=True)
#     users.create_index('email', unique=True)

#     # Seed sample lessons if empty
#     if lessons.count_documents({}) == 0:
#         sample = [
#             {
#                 'title': 'Past Simple Basics',
#                 'slug': 'past-simple-1',
#                 'description': 'Practice past simple tense.',
#                 'content': {'exercises': [
#                     {'id': 'ps-1', 'prompt': 'He _ to the market yesterday.', 'answer': 'went'}
#                 ]}
#             },
#             {
#                 'title': 'Subject-Verb Agreement',
#                 'slug': 'sv-agree-1',
#                 'description': 'Match verbs to subjects.',
#                 'content': {'exercises': [
#                     {'id': 'sv-1', 'prompt': 'She (go) to school every day.', 'answer': 'goes'}
#                 ]}
#             }
#         ]
#         lessons.insert_many(sample)


# import os
# from pymongo import MongoClient
# from dotenv import load_dotenv
# from datetime import datetime
# import logging
# logger = logging.getLogger(__name__)

# load_dotenv()

# MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
# DB_NAME = os.getenv("MONGO_DB", "english_tutor")

# client = MongoClient(MONGO_URL)
# db = client[DB_NAME]

# def init_db():
#     lessons = db['lessons']
#     users = db['users']
#     quiz_collection = db['quizzes']

#     # Ensure unique indexes
#     lessons.create_index('slug', unique=True)
#     users.create_index('email', unique=True)

#     # Seed sample lessons if empty
#     if lessons.count_documents({}) == 0:
#         sample_lessons = [
#             {
#                 'title': 'Past Simple Tense',
#                 'slug': 'past-simple-tense',
#                 'description': 'Master the past simple tense and its usage in English.',
#                 'notes': 'The past simple is used to talk about actions completed in the past. Formation: subject + past verb form + object. Regular verbs add -ed. Many common verbs are irregular.',
#                 'examples': [
#                     'She walked to the store yesterday.',
#                     'I didn\'t see the movie last week.',
#                     'Did they arrive on time?',
#                     'We lived in London for five years.',
#                     'He worked as a teacher before.'
#                 ]
#             },
#             {
#                 'title': 'Present Perfect',
#                 'slug': 'present-perfect',
#                 'description': 'Learn the present perfect tense for recent past events.',
#                 'notes': 'The present perfect connects the past to the present. Use: have/has + past participle. Useful for recent actions, life experiences, and unfinished time periods.',
#                 'examples': [
#                     'I have visited Paris three times.',
#                     'She has just finished her homework.',
#                     'They have lived here since 2015.',
#                     'Have you ever seen a polar bear?',
#                     'We haven\'t heard from them yet.'
#                 ]
#             },
#             {
#                 'title': 'Subject-Verb Agreement',
#                 'slug': 'subject-verb-agreement',
#                 'description': 'Ensure subjects and verbs agree in number and person.',
#                 'notes': 'The verb must agree with its subject in number (singular/plural) and person (1st, 2nd, 3rd). Common mistakes occur with collective nouns and phrases between subject and verb.',
#                 'examples': [
#                     'She plays tennis every weekend.',
#                     'The students are studying hard.',
#                     'Each of the boys has a unique talent.',
#                     'Neither my friends nor my brother agrees with me.',
#                     'The government has announced new policies.'
#                 ]
#             },
#             {
#                 'title': 'Conditional Sentences',
#                 'slug': 'conditional-sentences',
#                 'description': 'Master if-clauses and conditional structures.',
#                 'notes': 'Conditionals express hypothetical situations. Type 1 (likely), Type 2 (unlikely), Type 3 (impossible/past). Each has distinct grammar patterns and time references.',
#                 'examples': [
#                     'If it rains, we will stay home.',
#                     'If I were you, I would apologize.',
#                     'If they had studied, they would have passed.',
#                     'Unless you hurry, you will be late.',
#                     'Should you need help, call me.'
#                 ]
#             },
#             {
#                 'title': 'Comparative and Superlative',
#                 'slug': 'comparative-superlative',
#                 'description': 'Compare and rank things using adjectives.',
#                 'notes': 'Use -er/-est for short adjectives, more/most for longer ones. Comparative: bigger, more beautiful. Superlative: biggest, most beautiful. Irregular forms: good/better/best.',
#                 'examples': [
#                     'This book is more interesting than that one.',
#                     'She is the tallest person in the class.',
#                     'The weather today is worse than yesterday.',
#                     'That\'s the best decision you could make.',
#                     'My apartment is smaller but more comfortable.'
#                 ]
#             },
#             {
#                 'title': 'Passive Voice',
#                 'slug': 'passive-voice',
#                 'description': 'Transform active sentences to passive voice.',
#                 'notes': 'Passive voice emphasizes the action or receiver rather than the doer. Form: be + past participle. Use when the agent is unknown, obvious, or unimportant.',
#                 'examples': [
#                     'The cake was baked by Maria.',
#                     'English is spoken around the world.',
#                     'The project has been completed.',
#                     'The office will be renovated next month.',
#                     'The letter was written in 1920.'
#                 ]
#             },
#             {
#                 'title': 'Reported Speech',
#                 'slug': 'reported-speech',
#                 'description': 'Report what others have said indirectly.',
#                 'notes': 'Indirect speech reports what someone said without quoting exactly. Tense changes typically shift back one level. Pronouns and time references also change.',
#                 'examples': [
#                     'She said that she was tired.',
#                     'He told me he would call me later.',
#                     'They said they hadn\'t seen the movie.',
#                     'She asked if I wanted coffee.',
#                     'He explained that the train was delayed.'
#                 ]
#             },
#             {
#                 'title': 'Articles and Determiners',
#                 'slug': 'articles-determiners',
#                 'description': 'Use articles (a, an, the) and determiners correctly.',
#                 'notes': 'A/an for countable nouns (new info), the for specific nouns or known references. No article for generalizations. Common determiners: this, that, some, many, few.',
#                 'examples': [
#                     'I saw a cat and a dog. The cat was black.',
#                     'Can you lend me a pen? The pen on the desk works well.',
#                     'She is a doctor; she treats patients.',
#                     'I like many books, but I love this particular one.',
#                     'There are some apples in the basket.'
#                 ]
#             },
#             {
#                 'title': 'Phrasal Verbs',
#                 'slug': 'phrasal-verbs',
#                 'description': 'Master common phrasal verbs and their meanings.',
#                 'notes': 'Phrasal verbs combine a verb with a preposition or adverb. Many are two-part (verb + particle), some are three-part. Meaning often differs from individual words.',
#                 'examples': [
#                     'I set up a new account yesterday.',
#                     'Please turn off the lights before leaving.',
#                     'They are looking forward to the vacation.',
#                     'Can you figure out this puzzle?',
#                     'We ran into an old friend at the store.'
#                 ]
#             },
#             {
#                 'title': 'Question Formation',
#                 'slug': 'question-formation',
#                 'description': 'Form different types of questions correctly.',
#                 'notes': 'Yes/no questions invert subject and auxiliary. WH- questions start with question words. Tag questions check information. Follow subject-auxiliary word order rules.',
#                 'examples': [
#                     'Do you like pizza?',
#                     'Where have you been?',
#                     'She doesn\'t play tennis, does she?',
#                     'What time is the meeting?',
#                     'Have they finished their work?'
#                 ]
#             }
#         ]
        
#         # Insert lessons
#         lessons.insert_many(sample_lessons)
        
#         # Create quizzes for each lesson (will be detailed in quiz.py seed)
#         for i, lesson in enumerate(sample_lessons, 1):
#             db['quiz_lessons'].insert_one({
#                 'lesson_slug': lesson['slug'],
#                 'lesson_title': lesson['title'],
#                 'created_at': datetime.utcnow()
#             })

#     # Optional: Seed a demo user for testing if users collection is empty
#     if users.count_documents({}) == 0:
#         demo_user = {
#             "email": "demo@tutor.com",
#             "hashed_password": "$argon2id$v=19$m=102400,t=2,p=8$O3Q6N2...",  # hashed 'password'
#             "level": "beginner",
#             "predicted_level": "Beginner",
#             "confidence": 0.0,
#             "difficulty_adjustment": "Maintain",
#             "recommended_lessons": [],
#             "created_at": datetime.utcnow()
#         }
#         users.insert_one(demo_user)



import os
import logging
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv
from datetime import datetime

# ---- Load environment variables ----
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "english_tutor")

# ---- Setup logging ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- Connect to MongoDB ----
client = MongoClient(MONGO_URL)
db = client[DB_NAME]

def init_db():
    """
    Initialize database:
    - Ensure unique indexes
    - Seed sample lessons if empty
    - Create quizzes collection entries
    - Optional demo user
    """
    try:
        # ---- Collections ----
        lessons = db['lessons']
        users = db['users']
        quizzes = db['quizzes']
        lesson_progress = db['lesson_progress']

        # ---- Ensure unique indexes ----
        lessons.create_index('slug', unique=True)
        users.create_index('email', unique=True)
        quizzes.create_index([('lesson_slug', 1), ('quiz_type', 1)], unique=True)
        lesson_progress.create_index([('lesson_slug', 1), ('user_email', 1)], unique=True)
        logger.info("✅ MongoDB indexes ensured")

        # ---- Seed sample lessons if empty ----
        if lessons.count_documents({}) == 0:
            sample_lessons = [
                {
                    'title': 'Past Simple Tense',
                    'slug': 'past-simple-tense',
                    'description': 'Master the past simple tense and its usage in English.',
                    'notes': 'The past simple is used to talk about actions completed in the past. Formation: subject + past verb form + object. Regular verbs add -ed. Many common verbs are irregular.',
                    'examples': [
                        'She walked to the store yesterday.',
                        'I didn\'t see the movie last week.',
                        'Did they arrive on time?',
                        'We lived in London for five years.',
                        'He worked as a teacher before.'
                    ]
                },
                {
                    'title': 'Present Perfect',
                    'slug': 'present-perfect',
                    'description': 'Learn the present perfect tense for recent past events.',
                    'notes': 'The present perfect connects the past to the present. Use: have/has + past participle. Useful for recent actions, life experiences, and unfinished time periods.',
                    'examples': [
                        'I have visited Paris three times.',
                        'She has just finished her homework.',
                        'They have lived here since 2015.',
                        'Have you ever seen a polar bear?',
                        'We haven\'t heard from them yet.'
                    ]
                },
                # Add other lessons as needed...
            ]

            lessons.insert_many(sample_lessons)
            logger.info(f"✅ Seeded {len(sample_lessons)} sample lessons")

            # ---- Create quizzes placeholder for each lesson ----
            for lesson in sample_lessons:
                try:
                    quizzes.insert_one({
                        'lesson_slug': lesson['slug'],
                        'quiz_types': {},  # to be filled later
                        'created_at': datetime.utcnow()
                    })
                except DuplicateKeyError:
                    logger.warning(f"Quiz for lesson '{lesson['slug']}' already exists")

        # ---- Optional: Seed demo user if empty ----
        if users.count_documents({}) == 0:
            demo_user = {
                "email": "demo@tutor.com",
                "hashed_password": "$argon2id$v=19$m=102400,t=2,p=8$O3Q6N2...",  # hashed 'password'
                "level": "beginner",
                "predicted_level": "Beginner",
                "confidence": 0.0,
                "difficulty_adjustment": "Maintain",
                "recommended_lessons": [],
                "created_at": datetime.utcnow()
            }
            try:
                users.insert_one(demo_user)
                logger.info("✅ Demo user created: demo@tutor.com")
            except DuplicateKeyError:
                logger.warning("Demo user already exists")

    except Exception as e:
        logger.error(f"init_db failed: {e}")
        raise