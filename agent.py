import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)


# -------------------------------------------------
# Analyze Main Document
# -------------------------------------------------

def analyze_document(document_text):

    prompt = f"""
You are DocFlow AI, an intelligent document workflow agent.

Analyze the document below and return ONLY valid JSON.

Extract:

1. document_type
2. purpose
3. deadline
4. eligibility
5. required_documents
6. important_information
7. priority
8. recommended_actions

Priority must be one of:
LOW
MEDIUM
HIGH

Return exactly this JSON structure:

{{
    "document_type": "",
    "purpose": "",
    "deadline": "",
    "eligibility": [],
    "required_documents": [],
    "important_information": [],
    "priority": "",
    "recommended_actions": []
}}

DOCUMENT:
-------------------------
{document_text}
-------------------------
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    result = response.text.strip()

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:

        return {
            "error": "Gemini returned invalid JSON",
            "raw_response": result
        }


# -------------------------------------------------
# Verify Supporting Documents
# -------------------------------------------------

def verify_documents(required_documents, uploaded_documents):

    documents_text = ""

    for document in uploaded_documents:

        documents_text += f"""

DOCUMENT NAME:
{document['name']}

DOCUMENT CONTENT:
-------------------------
{document['text']}
-------------------------

"""

    prompt = f"""
You are DocFlow AI, an autonomous document verification agent.

A user has a document containing a list of required documents.

Required documents:
{json.dumps(required_documents, indent=2)}

The user has uploaded the following supporting documents:

{documents_text}

Your task:

1. Identify what type of document each uploaded file represents.
2. Match uploaded documents against required documents.
3. Determine which requirements are verified.
4. Determine which requirements are missing.
5. Identify unclear documents.
6. Give a confidence score from 0 to 100.
7. Recommend the next action.

IMPORTANT:
- Do not assume a document exists if it was not uploaded.
- Do not mark a requirement as verified merely because it is mentioned in another document.
- Match based on the actual document content.
- Return ONLY valid JSON.

Return exactly:

{{
    "verified_documents": [
        {{
            "required_document": "",
            "uploaded_file": "",
            "confidence": 0,
            "reason": ""
        }}
    ],
    "missing_documents": [],
    "unclear_documents": [
        {{
            "uploaded_file": "",
            "possible_type": "",
            "confidence": 0,
            "reason": ""
        }}
    ],
    "next_action": ""
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    result = response.text.strip()

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    try:

        return json.loads(result)

    except json.JSONDecodeError:

        return {
            "error": "Gemini returned invalid verification JSON",
            "raw_response": result
        }