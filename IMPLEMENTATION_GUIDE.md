# AI Language Tutor - Complete Implementation Guide

## Overview

This is a full-stack English learning platform with:
- **Backend**: FastAPI + MongoDB with ML-powered student level prediction
- **Frontend**: React with clean, learning-focused UI
- **ML Model**: Scikit-learn trained model for personalized learning paths
- **Quiz System**: 5 interactive quiz types per lesson
- **10 Lessons**: Comprehensive English grammar curriculum

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app with routes
│   ├── db.py                # MongoDB connection & initialization
│   ├── models.py            # Pydantic schemas
│   ├── schemas.py           # API schemas
│   ├── ml/
│   │   └── level_predictor.py   # ML model integration (joblib)
│   ├── routes/
│   │   ├── auth.py          # Authentication
│   │   ├── lessons.py       # Lesson endpoints
│   │   ├── quiz.py          # Quiz submission & retrieval
│   │   ├── progress.py      # User progress & metrics
│   │   └── exercises.py     # Exercise endpoints
│   ├── services/
│   │   ├── student_metrics.py   # Calculate metrics & update ML predictions
│   │   └── ai_service.py        # AI evaluation service
│   └── scripts/
│       └── seed_quizzes.py      # Seed quiz questions for all lessons

frontend/
├── src/
│   ├── pages/
│   │   ├── Dashboard.jsx        # Main dashboard with tabs
│   │   ├── Auth.jsx             # Login/signup
│   │   └── LandingPage.jsx      # Welcome page
│   ├── components/
│   │   ├── LessonCard.jsx       # Lesson card with progress
│   │   ├── Quiz.jsx             # Quiz component with 5 types
│   │   ├── ProgressPanel.jsx    # User metrics & ML predictions
│   │   └── FeedbackPanel.jsx    # Feedback display
│   ├── utils/
│   │   └── api.js               # API client
│   └── App.jsx                  # Main app

models/
└── student_level_model.pkl      # Pre-trained ML model
```

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MONGO_URL="mongodb://localhost:27017"
export MONGO_DB="tutor_db"
export ALLOW_ANON="1"  # For development without auth

# Run the server
uvicorn app.main:app --reload
```

### 2. Initialize Database

The database is automatically initialized on startup via `init_db()`. This will:
- Create 10 lessons with detailed content
- Create unique indexes
- Seed a demo user

To manually seed quizzes:
```bash
python -m app.scripts.seed_quizzes
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Visit `http://localhost:5173` (or your configured port)

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login

### Lessons
- `GET /api/lessons` - Get all lessons
- `GET /api/lessons/{slug}` - Get specific lesson

### Quiz
- `POST /api/quiz/submit` - Submit quiz answers
- `GET /api/quiz/lesson/{lesson_slug}` - Get quizzes for a lesson
- `GET /api/quiz/attempts/{lesson_slug}` - Get user's attempts
- `GET /api/quiz/summary` - Get summary of all attempts

### Progress
- `GET /api/progress` - Get user progress with ML predictions
- `GET /api/progress/export?format=csv` - Export progress

## 10 Lessons Included

1. **Past Simple Tense** - Master past actions
2. **Present Perfect** - Learn present perfect grammar
3. **Subject-Verb Agreement** - Ensure proper grammar
4. **Conditional Sentences** - If-clauses and conditions
5. **Comparative and Superlative** - Compare and rank
6. **Passive Voice** - Transform active to passive
7. **Reported Speech** - Indirect quotation
8. **Articles and Determiners** - Article usage
9. **Phrasal Verbs** - Common verb combinations
10. **Question Formation** - Form correct questions

Each lesson includes:
- **Notes**: Key grammatical points
- **Examples**: 5+ practical examples
- **5 Quiz Types**: 10 questions each
  - Multiple Choice
  - Fill in the Blank
  - True/False
  - Matching
  - Short Answer

## Quiz System

### 5 Quiz Types

1. **Multiple Choice** (MC)
   - 4 options per question
   - 1 correct answer
   - 1 mark per question

2. **Fill in the Blank** (FB)
   - Complete sentences
   - Case-insensitive matching
   - 1 mark per question

3. **True/False** (TF)
   - Statement evaluation
   - Binary answer
   - 1 mark per question

4. **Matching** (Match)
   - Pair items with definitions
   - 6 pairs per question
   - 3+ marks per question

5. **Short Answer** (SA)
   - Free text responses
   - Multiple acceptable answers
   - 2 marks per question

### Grading Logic

```python
- MC: Exact match → full marks
- FB: Case-insensitive match → full marks
- TF: Boolean comparison → full marks
- Match: All pairs correct → full marks
- SA: Check acceptable answers list → full marks

Quiz Score = (Marks Earned / Total Marks) × 100
```

## ML Model Integration

### Student Metrics Calculated

After each quiz submission, the system calculates:

```python
metrics = {
    "avg_score": float,           # Average quiz score (0-1)
    "attempts": int,              # Total quiz attempts
    "completion_rate": float,     # Completion percentage
    "avg_time_per_lesson": float, # Average time spent
    "recent_score_trend": float   # Change in recent scores
}
```

### ML Prediction

The pre-trained scikit-learn model predicts:

```python
{
    "predicted_level": "Beginner|Intermediate|Advanced",
    "confidence": float,                    # 0-1, max probability
    "difficulty_adjustment": "Decrease|Maintain|Increase",
    "recommended_lessons": List[str]        # Lesson recommendations
}
```

### How to Integrate Your Model

1. **Ensure model path**: `backend/models/student_level_model.pkl`
2. **Verify features order** in [level_predictor.py](backend/app/ml/level_predictor.py):
   - avg_score
   - attempts
   - completion_rate
   - avg_time_per_lesson
   - recent_score_trend

3. **Customization**:
   ```python
   # In backend/app/ml/level_predictor.py
   def _difficulty_action(level_idx: int):
       # Customize difficulty adjustment logic
   
   def _lesson_recommendation(level_idx: int):
       # Customize lesson recommendations
   ```

## Frontend Components

### Dashboard
- Clean, minimal UI
- Two tabs: Lessons & Progress
- No marketing elements
- Learning-focused design

### LessonCard
- Shows lesson title & description
- Displays attempt count & best score
- Progress bar for completed lessons
- Visual completion indicator

### Quiz Component
- Supports all 5 quiz types
- Real-time answer validation
- Instant feedback after submission
- Detailed results with marks breakdown
- Try again button for retakes

### ProgressPanel
- Shows ML-predicted level
- Model confidence score
- Student metrics dashboard
- Lesson-by-lesson performance
- Personalized recommendations
- Export to CSV

## Customization Guide

### Add More Lessons

Edit [db.py](backend/app/db.py) `init_db()`:

```python
sample_lessons = [
    {
        'title': 'Your Lesson',
        'slug': 'unique-slug',
        'description': 'Brief description',
        'notes': 'Key teaching points',
        'examples': ['Example 1', 'Example 2', ...]
    },
    # Add more...
]
```

Then seed quizzes via [seed_quizzes.py](backend/app/scripts/seed_quizzes.py)

### Customize Quiz Questions

Edit [seed_quizzes.py](backend/app/scripts/seed_quizzes.py) → `QUIZZES_DATA` dictionary

### Adjust ML Thresholds

In [level_predictor.py](backend/app/ml/level_predictor.py):

```python
LEVEL_MAP = {
    0: "Beginner",
    1: "Intermediate", 
    2: "Advanced"
}

def _difficulty_action(level_idx: int):
    # Modify logic based on your thresholds
```

### Style Customization

All CSS files are in `frontend/src/`:
- `pages/Dashboard.css` - Main layout
- `components/Quiz.css` - Quiz styling
- `components/LessonCard.css` - Card styles
- `components/ProgressPanel.css` - Progress display

## Database Schema

### users
```javascript
{
  _id: ObjectId,
  email: string,
  hashed_password: string,
  level: string,                    // "beginner", "intermediate", "advanced"
  predicted_level: string,          // From ML model
  confidence: number,               // 0-1
  difficulty_adjustment: string,    // "Decrease|Maintain|Increase"
  recommended_lessons: [string],    // Lesson slugs
  created_at: datetime
}
```

### lessons
```javascript
{
  _id: ObjectId,
  title: string,
  slug: string (unique),
  description: string,
  notes: string,
  examples: [string],
  created_at: datetime
}
```

### quiz_questions
```javascript
{
  _id: ObjectId,
  lesson_slug: string,
  lesson_title: string,
  quiz_type: string,               // "multiple_choice", "fill_blank", etc.
  total_marks: number,
  questions: [
    {
      question_id: string,
      quiz_type: string,
      question_text: string,
      // Type-specific fields...
      correct_answer: any,
      marks: number
    }
  ],
  created_at: datetime
}
```

### quiz_attempts
```javascript
{
  _id: ObjectId,
  user_email: string,
  lesson_slug: string,
  quiz_type: string,
  quiz_score: number,              // 0-100
  score_earned: number,
  total_marks: number,
  detailed_results: [
    {
      question_id: string,
      user_answer: any,
      correct: boolean,
      marks_awarded: number
    }
  ],
  submitted_at: datetime
}
```

## Testing

### Test a Quiz Submission

```bash
curl -X POST http://localhost:8000/api/quiz/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "lesson_slug": "past-simple-tense",
    "quiz_type": "multiple_choice",
    "questions_with_answers": [
      {"question_id": "mc1", "user_answer": "went"}
    ]
  }'
```

### Check User Progress

```bash
curl http://localhost:8000/api/progress \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Troubleshooting

### Model Not Loaded
- Check `models/student_level_model.pkl` exists
- Verify path in `level_predictor.py`
- Check features match: avg_score, attempts, completion_rate, avg_time_per_lesson, recent_score_trend

### Quizzes Not Showing
- Run `python -m app.scripts.seed_quizzes` to populate
- Check MongoDB connection
- Verify quiz_questions collection exists

### Frontend Not Updating
- Clear browser cache
- Check API token validity
- Verify CORS settings in `main.py`

### Import Errors
- Ensure all packages installed: `pip install -r requirements.txt`
- Check Python version (3.8+)
- Verify virtual environment activated

## Performance Tips

1. **Add MongoDB Indexes**:
   ```javascript
   db.lessons.createIndex({ "slug": 1 })
   db.users.createIndex({ "email": 1 })
   db.quiz_attempts.createIndex({ "user_email": 1, "lesson_slug": 1 })
   ```

2. **Cache Quiz Questions** in Frontend to reduce API calls

3. **Batch Update User Predictions** instead of per-quiz

4. **Optimize ML Model** - Consider quantization if model is large

## Deployment

### Backend (FastAPI)
```bash
# Production server
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Frontend (React)
```bash
# Build production bundle
npm run build

# Serve with static hosting
npm run preview
```

## Support

For issues or questions:
1. Check logs in terminal
2. Review API responses in browser DevTools
3. Verify MongoDB connection
4. Check environment variables are set

---

**Happy Learning! 🚀**
