# DocFlow AI

DocFlow AI is a smart document workflow assistant built with Python and Streamlit. It helps users upload a requirement document (such as a scholarship notice, internship brief, application form, or hackathon rule sheet), extract its text from PDF, analyze the content, and generate a structured workflow dashboard.

The app identifies:
- document type
- purpose and key details
- deadline and priority
- eligibility requirements
- required supporting documents
- missing items and verification status
- recommended next actions

## Features

- PDF upload and text extraction
- AI-powered document analysis using Google Gemini
- Eligibility and requirement detection
- Matching of uploaded supporting documents against required documents
- Missing-document tracking and recommendations
- Human approval workflow and action checklist
- Responsive Streamlit dashboard UI

## Project Structure

- `app.py` — main Streamlit application
- `agent.py` — AI document analysis and document verification logic
- `pdf_processor.py` — PDF text extraction using PyMuPDF
- `requirements.txt` — project dependencies
- `.env.example` — sample environment file

## Tech Stack

- Python
- Streamlit
- Google GenAI
- PyMuPDF
- Python-dotenv

## Prerequisites

- Python 3.10+
- A valid Google Gemini API key

## Installation

1. Clone the repository
2. Create a virtual environment (optional but recommended)
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

You can also use the provided `.env.example` file as a template.

## Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal in your browser.

## How It Works

1. Upload a PDF requirement document.
2. The app extracts text from the document.
3. Gemini analyzes the content and extracts key requirements.
4. Upload supporting documents to verify completeness.
5. The app matches uploaded files against required documents.
6. Review the generated workflow and approve it before continuing.

## Example Use Cases

- Scholarship application tracking
- Internship document verification
- Hackathon eligibility checks
- Institutional application workflows

## License

This project is currently unlicensed. Add a license if you plan to distribute it publicly.
