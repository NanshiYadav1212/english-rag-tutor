# Frontend-Backend Integration Guide

## Project Status: ✅ CONNECTED & READY

**Date**: December 17, 2025  
**Frontend Port**: 5173 (or 5174 if in use)  
**Backend Port**: 8000  
**Database**: MongoDB (english_tutor)

---

## Quick Start

### Prerequisites
- Node.js (for frontend)
- Python 3.10+ (for backend)
- MongoDB running on localhost:27017

### 1. Start Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 2. Seed Database (First Time Only)

```bash
cd backend/scripts
python seed_data.py
```

Expected output:
```
[*] Starting Database Seeding...
[+] Connected to MongoDB: english_tutor
[+] Inserted 10 lessons
[+] Inserted 10 quiz sets
[*] Data Verification: 10 lessons, 10 quizzes
[+] Seeding completed successfully!
```

### 3. Start Frontend

```bash
cd frontend
npm install  # If needed
npm run dev
```

Expected output:
```
VITE v5.4.21  ready in 1037 ms
➜  Local:   http://localhost:5173/ (or 5174)
```

### 4. Open Application

Navigate to: **http://localhost:5173** (or the port shown in terminal)

---

## Architecture Overview

### Frontend Stack
- **Framework**: React 18 with Vite
- **UI Components**: Custom CSS + Lucide React icons
- **HTTP Client**: Axios
- **Base URL**: http://localhost:8000/api

### Backend Stack
- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **Port**: 8000
- **API Prefix**: /api

### Database
- **Name**: english_tutor
- **Collections**:
  - `lessons` - 10 complete grammar lessons
  - `quizzes` - 10 quiz sets (50 questions per lesson)
  - `users` - (for authentication)
  - `progress` - (for tracking user progress)

---

## API Endpoints Connected

### Lessons API

```javascript
// Get all lessons
GET /api/lessons/
Response: Array of lesson objects

// Get specific lesson by slug
GET /api/lessons/{slug}
Example: /api/lessons/basics-of-english-grammar
Response: {
  _id: string,
  title: string,
  slug: string,
  description: string,
  difficulty: "Beginner|Intermediate|Advanced",
  estimated_time: number,
  notes: string,
  examples: array
}
```

### Quiz API

```javascript
// Get all quiz types for a lesson
GET /api/quiz/lesson/{lesson_slug}
Response: {
  lesson_slug: string,
  lesson_title: string,
  quiz_types: {
    multiple_choice: { questions: array },
    true_false: { questions: array },
    fill_in_blanks: { questions: array },
    match_following: { questions: array },
    short_answer: { questions: array }
  }
}

// Get specific quiz type
GET /api/quiz/quiz/{lesson_slug}/{quiz_type}

// Submit quiz answers
POST /api/quiz/submit
Body: {
  lesson_slug: string,
  quiz_type: string,
  answers: { [question_id]: answer }
}
Response: {
  score: number,
  total_marks: number,
  percentage: number,
  passed: boolean,
  results: array
}

// Get answer key (admin)
GET /api/quiz/answer-key/{lesson_slug}/{quiz_type}
```

---

## Frontend Components Connected

### 1. Dashboard (`src/pages/Dashboard.jsx`)
- **Status**: ✅ Connected
- **API Calls**:
  - `GET /api/lessons/` - Fetch all lessons
  - `GET /api/progress/export` - Export progress as CSV
- **Features**:
  - Displays lesson cards
  - Shows lesson selection
  - Manages quiz navigation

### 2. LessonDetail (`src/components/LessonDetail.jsx`)
- **Status**: ✅ Connected
- **API Calls**:
  - `GET /api/lessons/{slug}` - Fetch lesson content
- **Features**:
  - Displays full lesson content
  - Shows examples and explanations
  - Difficulty badge
  - Estimated time display

### 3. QuizInterface (`src/components/QuizInterface.jsx`)
- **Status**: ✅ Connected
- **API Calls**:
  - `GET /api/quiz/lesson/{lesson_slug}` - Fetch quiz types
  - `GET /api/quiz/quiz/{lesson_slug}/{quiz_type}` - Fetch specific quiz
  - `POST /api/quiz/submit` - Submit answers and get score
- **Features**:
  - Displays all 5 quiz types
  - Multiple choice with radio buttons
  - True/False options
  - Fill in the blanks
  - Match the following pairs
  - Short answer text input
  - Score calculation
  - Pass/Fail feedback (70% threshold)

### 4. LessonCard (`src/components/LessonCard.jsx`)
- **Status**: ✅ Connected
- **API Calls**:
  - `GET /api/quiz/attempts/{lesson_slug}` - Fetch quiz attempts
- **Features**:
  - Shows lesson progress
  - Displays best score
  - Completion status

### 5. ProgressPanel (`src/components/ProgressPanel.jsx`)
- **Status**: ✅ Connected
- **API Calls**:
  - `GET /api/progress` - Fetch user progress data
- **Features**:
  - Displays overall statistics
  - Shows completed lessons
  - Lesson performance metrics

---

## API Utility (`src/utils/api.js`)

```javascript
import axios from 'axios';

export function api(token) {
  const instance = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
      Authorization: token ? `Bearer ${token}` : ''
    }
  });

  return instance;
}
```

**Usage Example**:
```javascript
// In any component
const response = await api(token).get('/lessons/');
const lesson = await api(token).get('/lessons/basics-of-english-grammar');
```

---

## Lesson Slugs

All lessons are accessed by their slugs:

1. `basics-of-english-grammar` - Basics of English Grammar
2. `parts-of-speech` - Parts of Speech
3. `tenses` - Tenses
4. `subject-verb-agreement` - Subject–Verb Agreement
5. `active-passive-voice` - Active & Passive Voice
6. `direct-indirect-speech` - Direct & Indirect Speech
7. `sentence-structure` - Sentence Structure
8. `common-grammar-mistakes` - Common Grammar Mistakes
9. `paragraph-writing` - Paragraph Writing
10. `practical-english-daily-use` - Practical English for Daily Use

---

## Quiz Types

Each lesson has 5 quiz types with 10 questions each:

1. **multiple_choice** - Multiple choice questions (1 mark each)
2. **true_false** - True/False questions (1 mark each)
3. **fill_in_blanks** - Fill in the blanks (1 mark each)
4. **match_following** - Match pairs (5 marks per set, 2 sets)
5. **short_answer** - Short answer questions (2 marks each)

**Total marks per lesson**: 60 marks  
**Pass threshold**: 70%

---

## Testing the Integration

### Test 1: Fetch Lessons
```bash
curl http://localhost:8000/api/lessons/
```

Expected response:
```json
[
  {
    "_id": "...",
    "title": "Basics of English Grammar",
    "slug": "basics-of-english-grammar",
    "description": "...",
    "difficulty": "Beginner",
    "estimated_time": 45,
    "notes": "...",
    "examples": [...]
  },
  ...
]
```

### Test 2: Fetch Specific Lesson
```bash
curl http://localhost:8000/api/lessons/basics-of-english-grammar
```

### Test 3: Fetch Quiz for Lesson
```bash
curl http://localhost:8000/api/quiz/lesson/basics-of-english-grammar
```

### Test 4: Submit Quiz Answers
```bash
curl -X POST http://localhost:8000/api/quiz/submit \
  -H "Content-Type: application/json" \
  -d '{
    "lesson_slug": "basics-of-english-grammar",
    "quiz_type": "multiple_choice",
    "answers": {
      1: "correct_option",
      2: "correct_option",
      3: "correct_option"
    }
  }'
```

---

## Common Issues & Solutions

### Issue 1: "Cannot connect to backend"
**Solution**:
- Ensure backend is running: `http://localhost:8000/api/lessons/`
- Check CORS middleware is enabled in `backend/app/main.py`
- Verify MongoDB connection: `mongodb://localhost:27017/`

### Issue 2: "Lessons not showing"
**Solution**:
- Seed database: `cd backend/scripts && python seed_data.py`
- Clear browser cache
- Check browser console for errors

### Issue 3: "Quiz submission fails"
**Solution**:
- Verify answer format matches quiz type
- Check question IDs are integers
- Ensure lesson_slug and quiz_type are correct

### Issue 4: Port already in use
**Solution**:
- Frontend: Vite will automatically try next port (5174, 5175, etc.)
- Backend: Change port: `uvicorn app.main:app --port 8001`

---

## Development Workflow

### When Making Changes

**Frontend Changes**:
1. Edit file in `frontend/src/`
2. Vite automatically reloads (hot reload)
3. Check browser console for errors

**Backend Changes**:
1. Edit file in `backend/app/`
2. Uvicorn automatically reloads (--reload flag)
3. Check terminal for startup errors

**Database Changes**:
1. Clear and reseed: `cd backend/scripts && python seed_data.py`
2. Or update seed script and run again

### Adding New Features

**Frontend**:
1. Create component in `src/components/` or `src/pages/`
2. Import API utility: `import { api } from '../utils/api'`
3. Use in component: `await api(token).get('/endpoint')`

**Backend**:
1. Create route in `backend/app/routes/`
2. Add router to `main.py`: `app.include_router(router)`
3. Test with curl

---

## Project Files Reference

### Frontend
- `frontend/src/utils/api.js` - API configuration
- `frontend/src/pages/Dashboard.jsx` - Main dashboard
- `frontend/src/components/LessonDetail.jsx` - Lesson display
- `frontend/src/components/QuizInterface.jsx` - Quiz system
- `frontend/src/components/ProgressPanel.jsx` - Progress tracking

### Backend
- `backend/app/main.py` - FastAPI app and routes
- `backend/app/routes/lessons.py` - Lesson endpoints
- `backend/app/routes/quiz.py` - Quiz endpoints
- `backend/app/db.py` - MongoDB connection
- `backend/scripts/seed_data.py` - Database seeding

### Data
- `backend/scripts/lessons_and_quizzes.json` - Master lesson content
- `backend/scripts/quizzes_part1.json` through `quizzes_part5.json` - Quiz data

---

## Environment Variables

Create `.env` file if needed:

```
VITE_API_URL=http://localhost:8000/api
MONGODB_URI=mongodb://localhost:27017/english_tutor
```

---

## Deployment Checklist

- [ ] Backend running and accessible
- [ ] MongoDB seeded with all data
- [ ] Frontend loads without errors
- [ ] Dashboard displays lessons
- [ ] Lesson content loads correctly
- [ ] Quiz loads and submits
- [ ] Scores calculate correctly
- [ ] Browser console has no errors
- [ ] API responses include all required fields
- [ ] CORS is properly configured

---

## Next Steps

### Current Implementation
✅ Database with 10 lessons and 500 quiz questions  
✅ Backend API with all endpoints  
✅ Frontend dashboard and components  
✅ Quiz system with automatic grading  
✅ Frontend-backend integration  

### To Build Upon
- [ ] User authentication (login/signup)
- [ ] Progress tracking per user
- [ ] Leaderboards and rankings
- [ ] Detailed analytics dashboard
- [ ] Admin panel for content management
- [ ] Certificate generation
- [ ] Discussion forums
- [ ] Mobile responsiveness
- [ ] Performance optimization
- [ ] Error recovery and retry logic

---

## Support & Debugging

### Enable Debug Logging

**Frontend** - Check browser DevTools:
1. Open DevTools (F12)
2. Go to Console tab
3. Look for API call logs

**Backend** - Check terminal:
1. Look for endpoint hit logs
2. Check error tracebacks
3. Verify request/response JSON

### Useful Commands

```bash
# Check if ports are in use
# Windows
netstat -ano | findstr ":8000"
netstat -ano | findstr ":5173"

# Check MongoDB
mongosh
> use english_tutor
> db.lessons.count()
> db.quizzes.count()

# Restart backend
pkill -f "uvicorn"
cd backend && python -m uvicorn app.main:app --reload

# Restart frontend
pkill -f "vite"
cd frontend && npm run dev
```

---

**Status**: Ready for Development & Testing  
**Last Updated**: December 17, 2025  
**Version**: 1.0 - Full Integration Complete
