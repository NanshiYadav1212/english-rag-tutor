# Getting Started - 5 Minutes to Running

## Prerequisites Check ✓

Before you start, verify you have:

```powershell
# Windows PowerShell
mongod --version           # MongoDB installed
python --version           # Python 3.8+
npm --version             # Node.js 14+
```

If any are missing, install them first.

## Step 1: Start MongoDB

```powershell
# Windows - Open new PowerShell window and run:
mongod

# Should see: "[initandlisten] listening on port 27017"
```

Keep this window open.

## Step 2: Run the Application

### Option A: Automatic (Windows)
```powershell
cd d:\ai-language-tutor
.\run.bat
```

This will automatically:
- Install dependencies
- Seed quiz questions
- Start backend on http://localhost:8000
- Start frontend on http://localhost:5173

### Option B: Manual (More Control)

**Terminal 1 - Backend:**
```powershell
cd d:\ai-language-tutor\backend
pip install -r requirements.txt
python -m app.scripts.seed_quizzes
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```powershell
cd d:\ai-language-tutor\frontend
npm install
npm run dev
```

## Step 3: Open the Application

Open your browser and go to:

```
http://localhost:5173
```

## Step 4: Test It Works

1. **Create Account** (or use ALLOW_ANON mode)
2. **Select a Lesson** from the list
3. **Read the lesson** content (notes & examples)
4. **Take a Quiz** - Choose any quiz type:
   - Click "Practice Quiz" section
   - Select a quiz type (Multiple Choice, Fill Blank, etc.)
   - Answer all questions
   - Click "Submit Quiz"
5. **View Results** - See your score breakdown
6. **Check Progress** - Click "Progress" tab to see:
   - Your predicted learning level
   - ML model confidence
   - Your metrics
   - Lesson performance
7. **Export Progress** - Click "Export" to download CSV

## What Should Happen

### First Quiz
- You complete a quiz
- See your score (e.g., "75%")
- See detailed results (which questions correct/incorrect)

### After Multiple Quizzes
- Progress tab shows metrics:
  - Average Score: ~75%
  - Quiz Attempts: 5+
  - Recent Trend: ↑ improving
- ML Predicted Level shows (e.g., "Intermediate" with 85% confidence)
- Recommendations appear based on your level

### Export
- Click "Export" button
- CSV file downloads with all your quiz attempts
- Can open in Excel/Google Sheets

## Troubleshooting

### "Cannot connect to MongoDB"
- Ensure MongoDB is running (Terminal should show "listening on port 27017")
- If not, start it with `mongod`

### "Module not found" errors
- Backend: Run `pip install -r requirements.txt` in backend folder
- Frontend: Run `npm install` in frontend folder

### "Quizzes not found"
- Run: `python -m app.scripts.seed_quizzes` (from backend folder)
- Check MongoDB has data: Open Mongo Compass or mongosh

### "Frontend won't start"
- Kill any process on port 5173: `Get-Process -Name node | Stop-Process`
- Try: `npm run dev` again
- Check node_modules exists: `ls node_modules`

### "Port already in use"
- Backend port 8000: `Get-Process -Name python | Stop-Process`
- Frontend port 5173: `Get-Process -Name node | Stop-Process`

## Stopping the Application

- Press `Ctrl+C` in each terminal window
- Or close the terminal windows
- Or click stop in the task manager

## Next: Customization

After confirming everything works:

1. **Add more quizzes**: Edit `backend/app/scripts/seed_quizzes.py`
2. **Modify lessons**: Edit `backend/app/db.py`
3. **Change UI colors**: Edit `frontend/src/components/*.css`
4. **Adjust ML model**: Replace `backend/models/student_level_model.pkl`

See `IMPLEMENTATION_GUIDE.md` for detailed customization.

## Quick Reference

| URL | Purpose |
|-----|---------|
| http://localhost:5173 | Main app |
| http://localhost:8000 | Backend API |
| http://localhost:8000/docs | API documentation |
| http://localhost:8000/redoc | Alternative API docs |

## Terminal Window Layout

Recommended setup:
1. **MongoDB terminal** - Run `mongod` (background)
2. **Backend terminal** - Run backend server
3. **Frontend terminal** - Run frontend server
4. **Browser** - http://localhost:5173

## Common Commands

```powershell
# View all lessons
curl http://localhost:8000/api/lessons

# View user progress
curl http://localhost:8000/api/progress

# View MongoDB data
mongosh
> use tutor_db
> db.lessons.find().pretty()

# Check if ports are in use
netstat -ano | findstr :8000
netstat -ano | findstr :5173
```

## Support Commands

```powershell
# List all Python packages
pip list

# Check Node version
node --version
npm --version

# Test MongoDB connection
mongosh --eval "db.version()"

# Clear npm cache if having issues
npm cache clean --force
```

---

**You're all set! Open http://localhost:5173 and start learning! 🎓**

Need help? Check:
1. QUICK_START.md - Detailed checklist
2. IMPLEMENTATION_GUIDE.md - Full documentation
3. IMPLEMENTATION_SUMMARY.md - What was built
