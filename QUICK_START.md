# Quick Start Checklist

## Pre-flight Checks ✓

- [ ] MongoDB is running locally on `mongodb://localhost:27017`
- [ ] Python 3.8+ installed
- [ ] Node.js 14+ and npm installed
- [ ] `backend/models/student_level_model.pkl` exists

## Backend Setup

- [ ] Install dependencies: `cd backend && pip install -r requirements.txt`
- [ ] Create `.env` file with:
  ```
  MONGO_URL=mongodb://localhost:27017
  MONGO_DB=tutor_db
  ALLOW_ANON=1
  ```
- [ ] Start backend: `uvicorn app.main:app --reload`
- [ ] Backend running on `http://localhost:8000`

## Database Initialization

- [ ] Visit `http://localhost:8000/docs` (Swagger UI appears = backend OK)
- [ ] Lessons automatically seeded on first startup
- [ ] Seed quizzes: `python -m app.scripts.seed_quizzes` (from backend folder)
- [ ] Check MongoDB:
  ```bash
  mongosh
  use tutor_db
  db.lessons.count()      # Should be 10
  db.quiz_questions.count()  # Should be 50 (10 lessons × 5 types)
  ```

## Frontend Setup

- [ ] Install dependencies: `cd frontend && npm install`
- [ ] Start frontend: `npm run dev`
- [ ] Frontend running on `http://localhost:5173` (or shown in terminal)
- [ ] Dashboard loads without errors

## Functionality Testing

- [ ] **Login**: Create account or use ALLOW_ANON mode
- [ ] **View Lessons**: See all 10 lessons on dashboard
- [ ] **Read Lesson**: Click lesson card, view notes & examples
- [ ] **Take Quiz**: Select quiz type, answer questions, submit
- [ ] **See Results**: View score, correct/incorrect breakdown
- [ ] **Check Progress**: Switch to Progress tab, see:
  - [ ] ML-predicted level
  - [ ] Model confidence
  - [ ] Metrics (avg score, attempts, etc.)
  - [ ] Lesson performance stats
  - [ ] Recommendations
- [ ] **Export Progress**: Click Export button, download CSV

## API Integration Check

Test these endpoints:

```bash
# Get lessons
curl http://localhost:8000/api/lessons

# Get quiz for a lesson
curl http://localhost:8000/api/quiz/lesson/past-simple-tense

# View progress (requires auth token)
curl http://localhost:8000/api/progress \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "MongoDB connection refused" | Ensure MongoDB running: `mongod` |
| "Model not found" | Check `models/student_level_model.pkl` exists |
| "Quiz questions not found" | Run `python -m app.scripts.seed_quizzes` |
| "CORS errors" | Check backend CORS middleware is active |
| "Quiz won't submit" | Ensure all questions are answered |
| "Progress not updating" | Refresh page, check quiz was submitted |
| "ML predictions not showing" | Check quiz attempts exist in database |

## Next Steps

1. **Customize Lessons**: Edit `backend/app/db.py` to modify lesson content
2. **Add More Quiz Questions**: Edit `backend/app/scripts/seed_quizzes.py`
3. **Adjust ML Thresholds**: Modify `backend/app/ml/level_predictor.py`
4. **Style Changes**: Edit CSS files in `frontend/src/`
5. **Deploy**: Follow deployment guide in IMPLEMENTATION_GUIDE.md

## Quick Debug Commands

```bash
# Check Python packages
pip list | grep -E "fastapi|pymongo|scikit-learn|joblib"

# Test MongoDB connection
python -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017').server_info()"

# Check frontend dev server
curl http://localhost:5173

# Watch backend logs
tail -f backend.log  # If configured

# List all lessons
mongosh --eval "use tutor_db; db.lessons.find().pretty()"

# Count quiz attempts
mongosh --eval "use tutor_db; db.quiz_attempts.count()"
```

## Key Files You Need to Know

- **Backend Entry**: `backend/app/main.py`
- **Database Init**: `backend/app/db.py`
- **ML Integration**: `backend/app/ml/level_predictor.py`
- **Quiz Logic**: `backend/app/routes/quiz.py`
- **Metrics Calc**: `backend/app/services/student_metrics.py`
- **Frontend Entry**: `frontend/src/App.jsx`
- **Main Dashboard**: `frontend/src/pages/Dashboard.jsx`
- **Quiz UI**: `frontend/src/components/Quiz.jsx`
- **Progress Display**: `frontend/src/components/ProgressPanel.jsx`

## Success Indicators

✓ You'll know everything works when:
1. Dashboard loads with 10 lessons
2. Can select and view lesson details
3. Can take any of the 5 quiz types
4. Can see quiz results with scores
5. Progress tab shows ML-predicted level
6. Can export progress as CSV
7. Metrics update after each quiz

---

**You're all set! Start by accessing the frontend and taking your first quiz!** 🎓
