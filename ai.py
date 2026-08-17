import os
import json
from google import genai


def analyze_expense(text):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "shop": "Unknown",
            "amount": 0,
            "date": "Not Found",
            "category": "Other",
            "summary": "Gemini API key is not configured."
        }

    try:

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an AI expense analysis assistant.

Analyze this receipt OCR text.

Extract:
1. Shop name
2. Grand total amount
3. Date
4. Expense category

Choose ONLY one category:
Food, Shopping, Travel, Medical, Education, Bills, Other.

Give a short summary.

Return ONLY valid JSON:

{{
    "shop": "shop name",
    "amount": 0,
    "date": "date",
    "category": "category",
    "summary": "short summary"
}}

Receipt OCR text:
{text}
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        result = response.text.strip()

        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        data = json.loads(result)

        return data

    except Exception as e:

        print("Gemini AI Error:", e)

        return {
            "shop": "Unknown",
            "amount": 0,
            "date": "Not Found",
            "category": "Other",
            "summary": "AI analysis failed."
        }