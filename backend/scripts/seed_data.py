#!/usr/bin/env python3
"""
MongoDB Seed Script for English Grammar Learning Platform
Loads lesson and quiz data into MongoDB collections
"""

import json
import os
from pathlib import Path
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


class DatabaseSeeder:
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="english_tutor"):
        """Initialize MongoDB connection"""
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.client = None
        self.db = None
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            print(f"[+] Connected to MongoDB: {self.db_name}")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"[-] Failed to connect: {e}")
            return False
    
    def load_json_file(self, filepath):
        """Load JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[-] Error loading {filepath}: {e}")
            return None
    
    def seed_lessons(self, json_file):
        """Seed lessons collection"""
        data = self.load_json_file(json_file)
        if not data or 'lessons' not in data:
            return False
        
        try:
            self.db['lessons'].delete_many({})
            result = self.db['lessons'].insert_many(data['lessons'])
            self.db['lessons'].create_index('slug', unique=True)
            print(f"[+] Inserted {len(result.inserted_ids)} lessons")
            return True
        except Exception as e:
            print(f"[-] Error seeding lessons: {e}")
            return False
    
    def seed_quizzes(self, json_files):
        """Seed quizzes collection"""
        if isinstance(json_files, str):
            json_files = [json_files]
        
        try:
            self.db['quizzes'].delete_many({})
            all_quizzes = []
            for json_file in json_files:
                data = self.load_json_file(json_file)
                if data and 'quizzes' in data:
                    all_quizzes.extend(data['quizzes'])
            
            if not all_quizzes:
                return False
            
            result = self.db['quizzes'].insert_many(all_quizzes)
            self.db['quizzes'].create_index('lesson_slug')
            print(f"[+] Inserted {len(result.inserted_ids)} quiz sets")
            return True
        except Exception as e:
            print(f"[-] Error seeding quizzes: {e}")
            return False
    
    def verify_data(self):
        """Verify seeded data"""
        try:
            lessons = self.db['lessons'].count_documents({})
            quizzes = self.db['quizzes'].count_documents({})
            print(f"\n[*] Data Verification: {lessons} lessons, {quizzes} quizzes")
            return lessons > 0 and quizzes > 0
        except Exception as e:
            print(f"[-] Error verifying: {e}")
            return False
    
    def close(self):
        """Close connection"""
        if self.client:
            self.client.close()
    
    def run(self, lessons_file, quiz_files):
        """Run seeding"""
        print("[*] Starting Database Seeding...\n")
        
        if not self.connect():
            return False
        
        try:
            if not self.seed_lessons(lessons_file):
                return False
            if not self.seed_quizzes(quiz_files):
                return False
            
            if self.verify_data():
                print("\n[+] Seeding completed successfully!")
                return True
            return False
        finally:
            self.close()


def main():
    """Main"""
    script_dir = Path(__file__).parent
    # Use complete lessons file with 3 examples per lesson
    lessons_file = script_dir / 'lessons_complete.json'
    # Use comprehensive quizzes file with all 10 lessons (50 questions each)
    quiz_files = [script_dir / 'quizzes_all_lessons.json']
    
    # Fallback to original files if complete files don't exist
    if not lessons_file.exists():
        lessons_file = script_dir / 'lessons_and_quizzes.json'
    if not (script_dir / 'quizzes_all_lessons.json').exists():
        quiz_files = [
            script_dir / 'quizzes_part1.json',
            script_dir / 'quizzes_part2.json',
            script_dir / 'quizzes_part3.json',
            script_dir / 'quizzes_part4.json',
            script_dir / 'quizzes_part5.json'
        ]
    
    if not lessons_file.exists():
        print(f"[-] Lessons file not found")
        return 1
    
    seeder = DatabaseSeeder()
    success = seeder.run(str(lessons_file), [str(f) for f in quiz_files if Path(f).exists()])
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
