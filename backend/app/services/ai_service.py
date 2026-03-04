import os
import json
import traceback
from typing import Any, Dict, List
import httpx

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")


async def _call_openai_chat(prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [
            {"role": "system", "content": "You are an expert English teacher who provides corrections, concise explanations, and a numeric score between 0 and 1. Respond as JSON only."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(OPENAI_API_URL, headers=headers, json=body)
        resp.raise_for_status()
        return resp.json()


def _build_prompt(user_input: str, lesson_context: Dict[str, Any], user_level: str) -> str:
    ctx = {
        "lesson_context": lesson_context,
        "user_level": user_level,
        "user_input": user_input
    }

    # Guidance: ask for specific JSON fields
    return (
        "Given the following user input and lesson context, return a JSON object with keys:"
        "\n- correction: (string) the corrected version\n- explanations: (array of short strings) each explaining one correction\n- score: (float 0-1) a normalized proficiency score for this response\n- suggested_exercises: (array of strings) short suggestions for practice\n"
        "Respond with JSON only and nothing else.\n\nContext:\n" + json.dumps(ctx)
    )


async def evaluate_text(user_input: str, lesson_context: Dict[str, Any], user_level: str = "beginner") -> Dict[str, Any]:
    """Evaluate text using the configured AI provider.

    Returns a dict with keys: correction, explanations, score, suggested_exercises, raw_response
    Falls back to a safe default if the AI call fails.
    """
    try:
        prompt = _build_prompt(user_input, lesson_context or {}, user_level)
        if AI_PROVIDER == "openai":
            raw = await _call_openai_chat(prompt)
            # Try to extract assistant content
            content = None
            try:
                content = raw['choices'][0]['message']['content']
            except Exception:
                content = None

            if content:
                # strip markdown fences
                text = content.strip()
                text = text.replace('```json', '').replace('```', '').strip()
                try:
                    parsed = json.loads(text)
                except Exception:
                    # If AI returned plain text, attempt best-effort parsing
                    parsed = {"correction": text, "explanations": ["See corrected sentence."], "score": 0.75, "suggested_exercises": []}

                parsed['raw_response'] = raw
                return parsed

        # If provider not implemented or failed, raise to trigger fallback
        raise RuntimeError("AI provider not available or returned no content")

    except Exception as e:
        traceback.print_exc()
        # Fallback: return minimal evaluation without external AI
        fallback = {
            "correction": user_input,
            "explanations": ["AI service unavailable — returning your original input as fallback."],
            "score": 0.0,
            "suggested_exercises": [],
            "fallback": True,
            "error": str(e)
        }
        return fallback


def summarize_for_recommendation(evaluation: Dict[str, Any]) -> List[str]:
    """Utility to produce short suggested exercise titles from evaluation."""
    sug = evaluation.get('suggested_exercises') or []
    if sug:
        return sug
    # Infer simple suggestions from explanations
    exps = evaluation.get('explanations', [])
    out = []
    for e in exps[:3]:
        out.append(f"Practice: {e[:60]}")
    return out
