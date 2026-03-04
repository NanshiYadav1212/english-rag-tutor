# Enhanced React Dashboard with Multiple Lessons & Quizzes

This document outlines the updated React frontend components for the AI Language Tutor, now with full support for multiple lessons, quizzes, and progress tracking.

## New Components

### 1. `LessonCard.jsx` & `LessonCard.css`
A reusable card component for displaying lessons in the sidebar.

**Props:**
- `lesson`: lesson object with title, description, content (includes exercise count)
- `active`: boolean indicating if this lesson is currently selected
- `onClick`: callback to select the lesson

**Features:**
- Clean, minimal card design
- Shows lesson title and description
- Displays exercise count in the metadata
- Active state highlights the selected lesson
- Responsive hover effects

**Usage:**
```jsx
<LessonCard lesson={lesson} active={selectedLesson === lesson.slug} onClick={handleSelect} />
```

---

### 2. `Quiz.jsx` & `Quiz.css`
Manages exercise submission and feedback display for a lesson.

**Props:**
- `lessonId`: string identifier for the lesson
- `exercises`: array of exercise objects from `lesson.content.exercises`
  - Each exercise has: `id`, `prompt`, `type` ('free_text' or 'multiple_choice'), `options` (if MC)
- `token`: auth token for API calls

**Features:**
- Renders free-text input fields with submit buttons
- Supports multiple-choice exercises as button options
- Auto-submits when MC option is clicked
- Displays submission history below the input
- Integrates with `FeedbackPanel` to show feedback

**Exercise object structure:**
```javascript
{
  id: 'ex-1',
  prompt: 'Translate: "I go to school everyday"',
  type: 'free_text',
  // type: 'multiple_choice', options: ['A goes', 'He goes', 'They goes']
}
```

**Usage:**
```jsx
<Quiz lessonId={lessonId} exercises={lesson.content.exercises || []} token={token} />
```

---

### 3. Updated `LessonView.jsx`
Orchestrates lesson display, exercises, and submission history.

**Props:**
- `lessonId`: lesson slug/id
- `token`: auth token

**Flow:**
1. Fetches lesson data from `/lessons/{lessonId}`
2. Fetches user's submissions from `/progress` and filters by lessonId
3. Renders:
   - `LessonContent` (lesson intro, examples)
   - `Quiz` (exercises and submit UI)
   - `FeedbackPanel` list (previous submissions)

**Removed:**
- Old submit logic (now handled by Quiz component)
- Direct input state management

---

### 4. Updated `Dashboard.jsx`
Main dashboard with stats, lesson list, and lesson viewer.

**New Features:**
- Per-lesson average score displayed in lesson buttons
- Sparkline showing recent overall scores
- Loading/error states
- Lessons sidebar with quick stats:
  - Score percentage per lesson (e.g., "85%")
  - Quiz type hint (e.g., "free text")

**Data Flow:**
```
Dashboard
├── Fetch /lessons and /progress
├── Compute lesson-level averages from progress.recent
├── Render stats cards (total exercises, avg score, level, streak)
├── Render sparkline of recent scores
├── Render lessons sidebar with per-lesson scores
└── Render LessonView for selected lesson
```

---

### 5. Updated `FeedbackPanel.jsx`
Simplified to work with backend-driven feedback.

**Props:**
- `feedback`: submission object with `evaluation`, `user_input`, `_id`
- `token`: auth token for favorite toggling

**Evaluation object structure** (from backend):
```javascript
{
  correction: "I go to school every day.",
  explanations: [
    "Use 'go' (not 'goes') with 'I'",
    "Use 'every day' (two words)"
  ],
  score: 0.85,  // 0-1
  suggested_exercises: [
    "Practice subject-verb agreement",
    "Practice adverbs of frequency"
  ],
  fallback: false  // true if backend fell back (optional)
}
```

**Changes:**
- Removed Gemini/AI-specific parsing
- Simplified to expect flat evaluation object
- Shows fallback banner if `evaluation.fallback === true`
- Clean, focused UI

---

## Updated Styling

### `LessonCard.css`
```css
.lesson-card       /* main card button */
.lesson-card.active /* active state */
.lesson-card-body  /* title + description */
.lesson-card-title
.lesson-card-desc
.lesson-card-meta  /* exercise count */
```

### `Quiz.css`
```css
.quiz-root         /* container */
.quiz-title
.quiz-list         /* exercise list */
.quiz-item         /* single exercise */
.quiz-prompt       /* exercise text */
.quiz-input-row    /* input + submit */
.mc-options        /* multiple choice buttons */
.mc-opt            /* individual MC button */
.quiz-submissions  /* feedback history */
```

---

## Data Flow & Integration

### Backend Endpoints Used

1. **GET `/lessons`**
   - Returns array of lessons
   - Each lesson includes `content.exercises[]`

2. **GET `/lessons/{lessonId}`**
   - Returns single lesson with full content

3. **GET `/progress`**
   - Returns user progress: `{ count, avg_score, recent: [] }`
   - `recent[]` includes submissions with `evaluation`, `lesson_id`, `user_input`, `_id`

4. **POST `/exercises/submit`**
   - Payload: `{ lesson_id, user_input, mode }`
   - Returns: saved document with `evaluation`

5. **POST `/progress/favorite`** (optional)
   - Marks/unmarks submission as favorite

### Lesson Data Structure (Expected from Backend)

```javascript
{
  _id: 'lesson-1',
  slug: 'past-simple',
  title: 'Past Simple Tense',
  description: 'Learn to use past simple in English',
  content: {
    examples: [
      { sentence: 'I went to school', translation: 'Ich bin zur Schule gegangen' },
      // ...
    ],
    exercises: [
      {
        id: 'ex-1',
        prompt: 'Complete: "Yesterday I ___ to the park"',
        type: 'free_text'
      },
      {
        id: 'ex-2',
        prompt: 'Choose the correct form:',
        type: 'multiple_choice',
        options: ['He go', 'He goes', 'He went'],
        answer: 'He went'
      }
    ]
  }
}
```

---

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create .env with:
# OPENAI_API_KEY=sk_...
# ALLOW_ANON=1

uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` (or port shown by Vite).

---

## Adding New Lessons

To add a new lesson to the dashboard:

1. **Backend**: Seed lesson in DB or create POST `/lessons` endpoint:
   ```python
   db['lessons'].insert_one({
       'slug': 'gerunds',
       'title': 'Gerunds',
       'description': 'Practice gerunds and -ing forms',
       'content': {
           'examples': [...],
           'exercises': [
               {'id': 'ex-1', 'prompt': '...', 'type': 'free_text'},
               ...
           ]
       }
   })
   ```

2. **Frontend**: Dashboard auto-fetches and displays all lessons. No changes needed!

---

## Component Modularity

Each component is self-contained and can be reused:

- **LessonCard**: Use in any list view of lessons
- **Quiz**: Use for any quiz/exercise submission flow
- **FeedbackPanel**: Use to display feedback for any submission
- **LessonView**: Composable page combining the above

---

## Progress Tracking

- **Per-lesson score**: Calculated from all submissions for that lesson
- **Average score**: Mean of all submission scores
- **Level progression**: Auto-updated by backend based on `avg_score`:
  - `avg_score >= 0.88` → Advanced
  - `avg_score >= 0.75` → Intermediate
  - Otherwise → Beginner
- **Recommended path**: Auto-updated by backend to suggest weak lessons

---

## Fallback Handling

If backend service is unavailable:
- `FeedbackPanel` shows a banner: "Service unavailable — showing fallback result (original input)"
- User still sees their submission with `score: 0`
- No data loss; submissions stored with fallback flag
- When service recovers, can optionally re-evaluate

---

## Future Enhancements

1. **Batch Progress Export**: CSV export with per-lesson breakdown
2. **Achievement Badges**: Visual rewards for milestones (5 exercises, 0.9 avg score, etc.)
3. **Custom Quizzes**: Allow users to create and share custom lesson/exercise sets
4. **Spaced Repetition**: Smart scheduling of exercises based on performance
5. **Leaderboards**: Compare progress with other learners (opt-in)
6. **Multi-language Support**: Extend beyond English to other languages

---

## Troubleshooting

**Q: Lessons don't load on dashboard?**
- Check `/lessons` endpoint returns data
- Verify `lessonId` prop is passed correctly to `LessonView`

**Q: Quiz submissions fail?**
- Ensure `/exercises/submit` endpoint is working
- Check token is valid (check browser console for 401 errors)
- Verify lesson exists in DB

**Q: Feedback not displaying?**
- Confirm backend returns `evaluation` object
- Check `evaluation` has required keys: `correction`, `explanations`, `score`, `suggested_exercises`

**Q: Progress not updating?**
- Refresh dashboard to re-fetch `/progress`
- Verify submissions saved to `exercise_results` collection

---

## File Structure

```
frontend/src/
├── pages/
│   ├── Dashboard.jsx          (main hub)
│   ├── LessonView.jsx         (lesson viewer)
│   └── ...
├── components/
│   ├── LessonCard.jsx         (lesson card)
│   ├── LessonCard.css
│   ├── Quiz.jsx               (exercise handler)
│   ├── Quiz.css
│   ├── FeedbackPanel.jsx      (feedback display)
│   ├── LessonContent.jsx      (lesson intro)
│   └── ...
└── utils/
    └── api.js                 (axios instance)
```

---

End of Guide.
