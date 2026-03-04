# Backend: Local setup and secrets

This directory contains the FastAPI backend for the language tutor project.

Secrets and environment variables
AI integration
----------------

The project includes a modular AI adapter at `app/services/ai_service.py`.

Environment variables used:
- `AI_PROVIDER` (optional) — currently supports `openai` (default).
- `OPENAI_API_KEY` — required when `AI_PROVIDER=openai`.
- `OPENAI_API_URL` — optional custom endpoint (defaults to OpenAI's chat completions URL).
- `OPENAI_MODEL` — optional model id (default `gpt-4o-mini`).

To enable AI evaluation locally:

1. Install dependencies: `pip install -r requirements.txt` (httpx is used by the adapter).
2. Create a `.env` containing `OPENAI_API_KEY=your_key` (and other vars as needed).
3. Start the server as usual. Exercise submissions will call the AI and store the returned `evaluation` object in the `exercise_results` collection.

Notes on modularity:
- `app/services/ai_service.py` provides `evaluate_text(...)` which is used by the exercise and quiz routes. Swap implementations or add providers there if you want to use a different AI.
- The service returns a structured dict with `correction`, `explanations`, `score` (0-1), and `suggested_exercises`. If the AI call fails the service returns a `fallback` response and the backend stores that too.
  Google Cloud Console immediately and revoke the old key.
- Use `backend/.env.example` as a template. Copy it to `backend/.env` and
  fill in real values locally.

Quick start (Windows PowerShell)
```powershell
cd backend
# create virtualenv (optional)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# create .env from example and fill values
cp .env.example .env
# start server
$env:ALLOW_ANON='1'
uvicorn app.main:app --reload --port 8000
```

Security checklist
- Rotate any API keys that were exposed.
- Never commit `.env` to Git. Ensure `.gitignore` contains `/backend/.env`.
- Consider using a secrets manager (e.g., Google Secret Manager) for CI/deploy.
