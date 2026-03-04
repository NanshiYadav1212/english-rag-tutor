# Complete System Architecture

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Dashboard                                                │  │
│  │  ├─ Lessons Tab                                          │  │
│  │  │  ├─ LessonCard (list all lessons)                    │  │
│  │  │  └─ Quiz Component (5 types)                         │  │
│  │  └─ Progress Tab                                         │  │
│  │     └─ ProgressPanel (ML metrics display)               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          ↑         ↓                            │
│                      API Calls    JSON Response                 │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Routes                                                   │  │
│  │  ├─ /api/auth (login/signup)                           │  │
│  │  ├─ /api/lessons (get all lessons)                     │  │
│  │  ├─ /api/quiz                                          │  │
│  │  │  ├─ POST /submit (grade quiz)                       │  │
│  │  │  ├─ GET /lesson/{slug} (get quizzes)               │  │
│  │  │  ├─ GET /attempts/{slug}                            │  │
│  │  │  └─ GET /summary                                    │  │
│  │  └─ /api/progress                                      │  │
│  │     ├─ GET / (user metrics + predictions)              │  │
│  │     └─ GET /export (CSV export)                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          ↑         ↓                            │
│                     Services    Database Queries                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Services                                                 │  │
│  │  ├─ student_metrics.py                                  │  │
│  │  │  ├─ Compute metrics from attempts                    │  │
│  │  │  └─ Call ML model for predictions                   │  │
│  │  └─ ai_service.py (optional evaluation)                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ML Model Integration                                     │  │
│  │  └─ level_predictor.py                                  │  │
│  │     ├─ Load: models/student_level_model.pkl             │  │
│  │     ├─ Features: avg_score, attempts, completion_rate  │  │
│  │     │           avg_time, recent_trend                 │  │
│  │     └─ Output: level, confidence, recommendations      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          ↓                                      │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                    MONGODB (Database)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Collections                                              │  │
│  │  ├─ users                                                │  │
│  │  │  └─ {email, level, predicted_level,                 │  │
│  │  │     confidence, recommendations}                     │  │
│  │  ├─ lessons (10 lessons)                                │  │
│  │  │  └─ {title, slug, description, notes, examples}     │  │
│  │  ├─ quiz_questions (50 quizzes)                         │  │
│  │  │  └─ {lesson_slug, quiz_type, questions[]}           │  │
│  │  └─ quiz_attempts (user submissions)                    │  │
│  │     └─ {user_email, lesson_slug, quiz_type,            │  │
│  │        quiz_score, detailed_results, timestamp}        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Quiz Submission Flow

```
User Takes Quiz
    ↓
[Quiz.jsx] Form populated with 10 questions
    ↓
User answers all questions
    ↓
Click "Submit Quiz"
    ↓
[Dashboard] Sends POST /api/quiz/submit
{
  lesson_slug: "past-simple-tense",
  quiz_type: "multiple_choice",
  questions_with_answers: [
    {question_id: "mc1", user_answer: "went"},
    ...
  ]
}
    ↓
[quiz.py] Grade each answer
    ├─ MC: Exact match
    ├─ Fill Blank: Case-insensitive
    ├─ True/False: Boolean match
    ├─ Match: All pairs correct
    └─ Short Answer: Check acceptable_answers
    ↓
Calculate total_marks / marks_earned
    ↓
Store in quiz_attempts collection
    ↓
Call: student_metrics.update_user_learning_path(email)
    ├─ Compute metrics from ALL attempts
    ├─ Call ML model.predict(features)
    ├─ Get prediction (level, confidence, recommendations)
    └─ Update user document
    ↓
Return:
{
  ok: true,
  quiz_score: 75,
  score_earned: 15,
  total_marks: 20,
  detailed_results: [...]
}
    ↓
[Quiz.jsx] Show results page
    ↓
User can "Try Again"
    ↓
Or return to lessons
```

## ML Model Integration Flow

```
Quiz Submitted
    ↓
quiz_attempts stored in MongoDB
    ↓
Call: compute_student_metrics(email)
    ├─ Find all quiz_attempts for user
    ├─ Calculate:
    │  ├─ avg_score = sum(scores) / count
    │  ├─ attempts = count
    │  ├─ completion_rate = 1.0 (all submitted)
    │  ├─ avg_time_per_lesson = sum(times) / count
    │  └─ recent_score_trend = recent_5_avg - previous_avg
    └─ Return metrics dict
    ↓
metrics = {
  avg_score: 0.75,
  attempts: 5,
  completion_rate: 1.0,
  avg_time_per_lesson: 0.0,
  recent_score_trend: 0.05
}
    ↓
Call: predict_learning_path(metrics)
    ├─ Load model from: models/student_level_model.pkl
    ├─ Create features array: [avg_score, attempts, completion_rate, ...]
    ├─ model.predict(features) → level_idx (0, 1, 2)
    ├─ model.predict_proba(features) → [p0, p1, p2]
    ├─ Map: 0→Beginner, 1→Intermediate, 2→Advanced
    ├─ confidence = max(probabilities)
    ├─ difficulty_action: Decrease/Maintain/Increase
    └─ recommendations: ["Lesson1", "Lesson2", ...]
    ↓
prediction = {
  predicted_level: "Intermediate",
  confidence: 0.87,
  difficulty_adjustment: "Increase",
  recommended_lessons: ["Conditional Sentences", "Passive Voice"]
}
    ↓
Update users collection:
{
  predicted_level: "Intermediate",
  confidence: 0.87,
  difficulty_adjustment: "Increase",
  recommended_lessons: [...],
  last_updated: now
}
    ↓
Frontend fetches GET /api/progress
    ↓
[ProgressPanel] Displays:
  - Predicted Level badge
  - Confidence bar
  - Metrics cards
  - Recommendations
```

## Component Hierarchy

```
App.jsx
├─ Auth (login/signup)
├─ LandingPage (welcome)
└─ Dashboard (main)
   ├─ Header
   │  ├─ Title & Logo
   │  ├─ Export Button
   │  └─ Logout Button
   ├─ Navigation Tabs
   │  ├─ Lessons Tab (active)
   │  └─ Progress Tab
   └─ Content Area
      ├─ Lessons Tab Content
      │  ├─ Lessons Grid
      │  │  ├─ LessonCard 1
      │  │  ├─ LessonCard 2
      │  │  └─ ... (10 total)
      │  ├─ Lesson Detail Panel
      │  │  ├─ Lesson Content
      │  │  │  ├─ Title
      │  │  │  ├─ Description
      │  │  │  ├─ Notes
      │  │  │  └─ Examples
      │  │  └─ Quiz Component
      │  │     ├─ Quiz Type Selector (5 types)
      │  │     ├─ Questions Display
      │  │     ├─ Answer Inputs
      │  │     └─ Results Page
      │  │        ├─ Score Display
      │  │        ├─ Results Detail
      │  │        └─ Try Again Button
      │  └
      └─ Progress Tab Content
         └─ ProgressPanel
            ├─ ML Level Card
            │  ├─ Level Badge
            │  ├─ Confidence Bar
            │  └─ Difficulty Action
            ├─ Metrics Grid
            │  ├─ Average Score Card
            │  ├─ Attempts Card
            │  ├─ Completion Rate Card
            │  └─ Recent Trend Card
            ├─ Lesson Performance Table
            │  ├─ Attempts column
            │  ├─ Average Score column
            │  └─ Best Score column
            ├─ Recommendations Section
            └─ Summary Text
```

## Database Schema Details

### users Collection
```javascript
{
  _id: ObjectId,
  email: "user@example.com",
  hashed_password: "...",
  level: "beginner",
  predicted_level: "Intermediate",      // Updated by ML model
  confidence: 0.87,                     // Model confidence (0-1)
  difficulty_adjustment: "Increase",    // Recommendation
  recommended_lessons: [                // ML recommendations
    "Conditional Sentences",
    "Passive Voice"
  ],
  created_at: ISODate("2024-12-17T..."),
  last_updated: ISODate("2024-12-17T...")
}
```

### lessons Collection
```javascript
{
  _id: ObjectId,
  title: "Past Simple Tense",
  slug: "past-simple-tense",
  description: "Master the past simple tense...",
  notes: "The past simple is used for actions...",
  examples: [
    "She walked to the store yesterday.",
    "I didn't see the movie...",
    ...
  ],
  created_at: ISODate("2024-12-17T...")
}
```

### quiz_questions Collection
```javascript
{
  _id: ObjectId,
  lesson_slug: "past-simple-tense",
  lesson_title: "Past Simple Tense",
  quiz_type: "multiple_choice",        // 5 types
  total_marks: 10,
  questions: [
    {
      question_id: "mc1",
      quiz_type: "multiple_choice",
      question_text: "What is the past simple form of 'go'?",
      options: ["go", "went", "gone", "going"],
      correct_answer: "went",
      marks: 1
    },
    ... (10 questions)
  ],
  created_at: ISODate("2024-12-17T...")
}
```

### quiz_attempts Collection
```javascript
{
  _id: ObjectId,
  user_email: "user@example.com",
  lesson_slug: "past-simple-tense",
  quiz_type: "multiple_choice",
  quiz_score: 75,                      // 0-100 percentage
  score_earned: 15,                    // 15 out of 20 marks
  total_marks: 20,
  detailed_results: [
    {
      question_id: "mc1",
      user_answer: "went",
      correct: true,
      marks_awarded: 1
    },
    ... (for each question)
  ],
  submitted_at: ISODate("2024-12-17T...")
}
```

## API Response Examples

### GET /api/progress
```json
{
  "count": 5,
  "metrics": {
    "avg_score": 0.75,
    "attempts": 5,
    "completion_rate": 1.0,
    "avg_time_per_lesson": 0.0,
    "recent_score_trend": 0.05
  },
  "predicted_level": "Intermediate",
  "confidence": 0.87,
  "difficulty_adjustment": "Increase",
  "recommended_lessons": ["Passive Voice", "Reported Speech"],
  "lessons_stats": [
    {
      "lesson_slug": "past-simple-tense",
      "attempts": 2,
      "average_score": 80,
      "best_score": 85
    }
  ]
}
```

### POST /api/quiz/submit
```json
{
  "ok": true,
  "quiz_score": 75,
  "score_earned": 15,
  "total_marks": 20,
  "detailed_results": [
    {
      "question_id": "mc1",
      "user_answer": "went",
      "correct": true,
      "marks_awarded": 1
    }
  ]
}
```

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: MongoDB
- **ML**: Scikit-learn, joblib
- **API Auth**: JWT tokens
- **Password**: argon2
- **Data Validation**: Pydantic

### Frontend
- **Framework**: React 18+
- **Build**: Vite
- **UI**: Custom CSS + Lucide icons
- **API Client**: axios/fetch
- **State**: React hooks

### Infrastructure
- **Backend Port**: 8000
- **Frontend Port**: 5173
- **Database Port**: 27017 (MongoDB)

## Performance Considerations

1. **API Calls**:
   - Batch quiz questions loading
   - Cache progress data on frontend
   - Debounce frequent updates

2. **Database**:
   - Indexes on email, slug, user_email
   - Consider pagination for large datasets

3. **ML Model**:
   - Loaded once at startup
   - Predictions cached until new attempt
   - Consider async processing for heavy models

4. **Frontend**:
   - Lazy load lesson components
   - Debounce progress updates
   - Virtualize long lists

## Security Considerations

1. **Authentication**:
   - JWT tokens for session management
   - Argon2 password hashing
   - Token expiration (1 day default)

2. **Authorization**:
   - Verify user owns data
   - Validate quiz answers server-side
   - Prevent answer tampering

3. **Data Validation**:
   - Pydantic schemas validate all inputs
   - Sanitize quiz answers
   - Prevent SQL injection (MongoDB safe)

## Deployment Checklist

- [ ] Environment variables configured
- [ ] MongoDB connection tested
- [ ] ML model file present
- [ ] CORS headers set correctly
- [ ] JWT secret changed
- [ ] Database backed up
- [ ] Frontend build optimized
- [ ] Error logging configured
- [ ] Rate limiting enabled
- [ ] HTTPS enforced

---

**This architecture is scalable, maintainable, and ready for production!**
