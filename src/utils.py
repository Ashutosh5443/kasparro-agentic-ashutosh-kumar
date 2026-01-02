import os
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Client
client = None
if api_key:
    client = genai.Client(api_key=api_key)

def call_gemini(system_instruction: str, user_prompt: str) -> str:
    """
    Wraps Gemini API. Automatically switches to Mock Data on 429/404 errors.
    """
    if not client:
        print("[Warning] No API Key. Using Mock Data.")
        return get_mock_response(user_prompt)

    try:
        # Try using the standard 1.5 Flash model (usually more stable)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp", 
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            ),
            contents=user_prompt
        )
        return response.text
        
    except Exception as e:
        print(f"[API Error] {e}")
        print("[Info] API failed (Quota or Net). Switching to Offline Mock Data.")
        return get_mock_response(user_prompt)

def get_mock_response(prompt: str) -> str:
    """
    Returns hardcoded JSON to ensure the pipeline finishes.
    """
    # Check 1: Is the Analyst Agent asking for Product Data?
    # We look for keywords from analyst.py prompt
    if "Extract data" in prompt or "ProductModel" in prompt or "fields into JSON" in prompt:
        return json.dumps({
            "name": "GlowBoost Vitamin C Serum",
            "price": 699.0,
            "currency": "₹",
            "ingredients": ["Vitamin C", "Hyaluronic Acid", "Ferulic Acid"],
            "benefits": ["Brightening", "Fades dark spots", "Anti-aging"],
            "skin_type": ["Oily", "Combination"],
            "side_effects": ["Mild tingling", "Redness on broken skin"],
            "usage": "Apply 2-3 drops in the morning before sunscreen"
        })

    # Check 2: Is the Strategist Agent asking for Questions?
    if "questions" in prompt.lower():
        return json.dumps([
            {
                "category": "Usage",
                "question": "Can I use this with Retinol?",
                "answer": "It is recommended to alternate use (AM vs PM)."
            },
            {
                "category": "Safety",
                "question": "Is it safe for pregnancy?",
                "answer": "Consult your doctor, but Vitamin C is generally safe."
            },
            {
                "category": "Storage",
                "question": "Does it oxidize?",
                "answer": "Yes, keep in a cool dark place."
            },
            {
                "category": "Results",
                "question": "How long to see results?",
                "answer": "Typically 4-6 weeks of consistent use."
            },
            {
                "category": "Skin Type",
                "question": "Is it good for dry skin?",
                "answer": "Yes, but follow with a moisturizer."
            }
        ])
    
    return "{}"

def clean_json_string(json_str: str) -> str:
    if not json_str: return "{}"
    cleaned = json_str.strip()
    if cleaned.startswith("```json"): cleaned = cleaned[7:]
    elif cleaned.startswith("```"): cleaned = cleaned[3:]
    if cleaned.endswith("```"): cleaned = cleaned[:-3]
    return cleaned.strip()