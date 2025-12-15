# 🧠 AI Memory & Personality Engine

A full-stack AI system that gives Large Language Models (LLMs) long-term memory and adaptive personality traits.

## 🏗 Architecture
The system follows a modular client-server architecture:
- **Backend (FastAPI):** Handles psychographic memory extraction and persona injection.
- **Frontend (Streamlit):** Provides an interactive UI for chat ingestion and testing.
- **Intelligence (OpenAI):** Uses GPT-4o-mini for low-latency analysis.

## ✨ Key Features
- **Psychographic Extraction:** Converts raw chat logs into structured JSON (User Preferences, Emotional Patterns, Facts).
- **Strict Validation:** Uses `Pydantic` to ensure memory integrity.
- **Dynamic Personas:** "Hot-swappable" personalities (e.g., Therapist, Witty Friend) that adapt based on extracting memory.

## 🚀 Setup & Run (Windows CMD)

### 0. Prerequisite: Environment
Run this from the root folder to create and activate the virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate

1. Configuration
OPENAI_API_KEY=sk-proj-your-key-here

2. Backend Setup
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

3. Frontend Setup
cd frontend
pip install -r requirements.txt
streamlit run app.py