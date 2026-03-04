# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# _tokenizer = None
# _model = None

# def get_llm():
#     global _tokenizer, _model
#     if _model is None:
#         print("Loading LLM model...")
#         _tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
#         _model = AutoModelForCausalLM.from_pretrained(
#             "microsoft/phi-2",
#             device_map="auto",
#             torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
#         )
#     return _tokenizer, _model

# def generate(prompt):
#     tokenizer, model = get_llm()
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
#     output = model.generate(**inputs, max_new_tokens=400)
#     return tokenizer.decode(output[0], skip_special_tokens=True)


# import os
# from dotenv import load_dotenv
# import requests

# # Load environment variables from .env
# load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")
# API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"  # Google Gemini API endpoint

# def generate(prompt):
#     if not API_KEY:
#         raise ValueError("Please set GEMINI_API_KEY in your .env file")

#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "prompt": prompt,
#         "max_tokens": 400
#     }

#     response = requests.post(API_URL, json=data, headers=headers)
#     if response.status_code != 200:
#         raise ValueError(f"API error: {response.status_code}, {response.text}")

#     result = response.json()
#     return result.get("text", "")



# import os
# import requests
# from pathlib import Path
# from dotenv import load_dotenv

# # 1. Improved path handling to find the .env file in the backend root
# # __file__ is 'backend/app/rag/llm.py', so we go up 3 levels to reach 'backend/'
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# load_dotenv(dotenv_path=BASE_DIR / ".env")

# API_KEY = os.getenv("GEMINI_API_KEY")

# # Correct Gemini endpoint (Using gemini-1.5-flash as it is faster and cheaper for RAG)
# API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# def generate(prompt):
#     if not API_KEY:
#         # Debug print to help you see where it's looking
#         print(f"Searching for .env at: {BASE_DIR}")
#         raise ValueError("Please set GEMINI_API_KEY in your .env file")

#     # Gemini uses a query parameter for the key or a specific header
#     params = {"key": API_KEY}
#     headers = {"Content-Type": "application/json"}

#     # Gemini API requires this specific nested structure
#     data = {
#         "contents": [
#             {
#                 "parts": [{"text": prompt}]
#             }
#         ],
#         "generationConfig": {
#             "maxOutputTokens": 400,
#             "temperature": 0.7
#         }
#     }

#     try:
#         response = requests.post(API_URL, params=params, json=data, headers=headers)
        
#         # Check for HTTP errors
#         if response.status_code != 200:
#             raise ValueError(f"API error: {response.status_code}, {response.text}")

#         result = response.json()
        
#         # Safely navigate the response JSON to get the text
#         return result['candidates'][0]['content']['parts'][0]['text']

#     except (KeyError, IndexError) as e:
#         print(f"Parsing Error: {e}")
#         return "I'm sorry, I couldn't process the response from the AI."
#     except Exception as e:
#         print(f"Request Error: {e}")
#         return "An unexpected error occurred while contacting the AI."

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# 1. Absolute path handling for the .env file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

# 2. UPDATED MODEL: Using the stable 2025 Flash model
# gemini-1.5-flash is retired; gemini-2.5-flash is the new standard
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def generate(prompt):
    if not API_KEY:
        print(f"ERROR: API Key not found. Checking path: {BASE_DIR / '.env'}")
        raise ValueError("Please set GEMINI_API_KEY in your .env file")

    # Use the format verified in your test.py
    url = f"{API_URL}?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "maxOutputTokens": 2048,
            "temperature": 0.4
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code != 200:
            # This will print the specific reason if it fails again
            print(f"!!! GEMINI API ERROR: {response.status_code} - {response.text}")
            return "I'm sorry, I'm having trouble connecting to my brain right now."

        result = response.json()
        
        # Safe extraction of the text response
        return result['candidates'][0]['content']['parts'][0]['text']

    except Exception as e:
        print(f"!!! CRITICAL SYSTEM ERROR: {str(e)}")
        return "System error: Failed to process the request."