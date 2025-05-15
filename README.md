AI Concierge for Small-Business AI Adoption

An AI-powered assistant designed to support small businesses in adopting artificial intelligence. It answers AI-related queries, schedules demo calls, manages to-do lists, self-assesses retrieved information, and adapts based on user feedback.

🚀 Features

✅ Core Functionality

FastAPI backend with async endpoints and JWT authentication

RAG (Retrieval-Augmented Generation) using ChromaDB and HuggingFace embeddings

Self-Grading of retrieved content with relevance and coverage scores

Self-Reflection adapting responses based on feedback

Task Management to schedule and list to-dos

🎙 Voice Interface (Bonus)

Future-ready endpoints for STT (Speech-to-Text) and TTS (Text-to-Speech)

🧠 Technologies Used

FastAPI, Uvicorn, Pydantic

LangChain, LangChain-Community, LangChain-HuggingFace

ChromaDB for vector search

HuggingFace Embeddings

JWT & Python-Jose for secure authentication

SlowAPI for rate limiting

Docker & Docker Compose

🛠️ Setup Instructions

🔧 Local Development

# Clone the repository
https://github.com/YOUR_USERNAME/ai-concierge-small-business-ai.git
cd ai-concierge-small-business-ai

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Launch the server
uvicorn main:app --reload

🐳 Docker Setup

docker compose up --build

Access API Docs at: http://localhost:8000/docs

🧪 API Testing Guide

🔐 Authentication

Register:

POST /register
{
  "username": "admin",
  "password": "secret"
}

Login:

POST /login
{
  "username": "admin",
  "password": "secret"
}

✅ Returns: access_token

💬 Chat Endpoint

POST /concierge/chat
Header: Authorization: Bearer <access_token>
Body: {
  "message": "What is few-shot learning?"
}

🧠 Feedback Commands

Body: {"message": "/good_answer"}  # or /bad_answer

🤖 Self-Grading Logic

Every RAG call is followed by self-grading:

Rates Relevance and Coverage from 0 to 1

If either score < 0.6:

Re-queries with refined prompt

If still low → responds with fallback message

Example:

"📭 Sorry, my knowledge base doesn't cover that topic."

🪞 Self-Reflection Algorithm

Tracks user feedback via /good_answer or /bad_answer

Applies decay factor 0.5 each turn

Adjusts response tone accordingly

Score

Prompt Adjustment

> 0

Maintain current style

< 0

Be more concise and cite sources explicitly

📋 To-Do List Functionality

Used for scheduling AI demos, follow-ups, etc.

# Add task
manage_tasks("add", task={"title": ..., "when": ..., "description": ...})

# List tasks
manage_tasks("list")

📦 Project Structure

.
├── main.py                    # Main FastAPI app
├── auth.py                   # JWT auth utilities (optional modularization)
├── requirements.txt          # Dependencies
├── Dockerfile                # Image build
├── docker-compose.yml        # Multi-service config
└── chroma_db/                # Vector store persistence

🧪 Testing Suite (to add)

✅ Unit tests for:

retrieve_docs

self_grade

manage_tasks

✅ Integration tests for:

/register

/login

/concierge/chat
