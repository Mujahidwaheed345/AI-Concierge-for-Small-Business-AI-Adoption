# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# # Simulated tools (you’ll import real ones later)
# from typing import List

# app = FastAPI()

# # Allow frontend or Postman to talk to this
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------- Models --------
# class ChatInput(BaseModel):
#     message: str

# # -------- In-memory state --------
# feedback_score = 0.0
# task_list = []

# # -------- Utilities (simulated) --------
# def update_feedback(command: str):
#     global feedback_score
#     if command == "/good_answer":
#         feedback_score += 1
#     elif command == "/bad_answer":
#         feedback_score -= 1
#     feedback_score *= 0.5
#     return feedback_score

# def get_prompt():
#     if feedback_score < 0:
#         return "Be more concise and cite sources explicitly."
#     elif feedback_score > 0:
#         return "Maintain current style, user is satisfied."
#     else:
#         return "Respond normally."

# def manage_tasks(action: str, task: dict = None):
#     if action == "add" and task:
#         task_list.append(task)
#         return f"Task added: {task['title']}"
#     elif action == "list":
#         return task_list
#     return "Invalid action."

# # -------- Endpoint: Chat --------
# @app.post("/concierge/chat")
# async def chat(input: ChatInput):
#     user_msg = input.message.strip()

#     # Feedback commands
#     if user_msg in ["/good_answer", "/bad_answer"]:
#         new_score = update_feedback(user_msg)
#         return {"feedback_score": new_score, "prompt": get_prompt()}

#     # Task-related command (demo)
#     if "schedule" in user_msg.lower():
#         manage_tasks("add", {
#             "title": "Demo Call",
#             "when": "Thursday 3 PM",
#             "description": "AI concierge demo"
#         })
#         return {"response": "✅ Demo call scheduled for Thursday at 3 PM."}

#     # Fallback answer
#     return {"response": f"🤖 I'm still learning. (Pretending to answer: '{user_msg}')"}
# from langchain.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.documents import Document
# from typing import List
# # Load existing ChromaDB vector store
# embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)

# # ---------- retrieve_docs ----------
# def retrieve_docs(query: str):
#     results = vectorstore.similarity_search_with_score(query, k=3)
#     docs = []
#     for doc, score in results:
#         docs.append({
#             "content": doc.page_content,
#             "source": doc.metadata.get("source", "unknown"),
#             "metadata": doc.metadata
#         })
#     return {"docs": docs, "query": query}
# def self_grade(question: str, docs: List[dict]):
#     # Simulated self-grading (replace with GPT call later if needed)
#     if not docs:
#         return {"relevance": 0.0, "coverage": 0.0}

#     # Basic logic: if any doc contains a word from the question, it's relevant
#     relevance = 0.8 if any(q in docs[0]['content'].lower() for q in question.lower().split()) else 0.4
#     coverage = 0.7 if len(docs) > 1 else 0.5
#     return {"relevance": relevance, "coverage": coverage}
# @app.post("/concierge/chat")
# async def chat(input: ChatInput):
#     user_msg = input.message.strip()

#     if user_msg in ["/good_answer", "/bad_answer"]:
#         new_score = update_feedback(user_msg)
#         return {"feedback_score": new_score, "prompt": get_prompt()}

#     if "schedule" in user_msg.lower():
#         manage_tasks("add", {
#             "title": "Demo Call",
#             "when": "Thursday 3 PM",
#             "description": "AI concierge demo"
#         })
#         return {"response": "✅ Demo call scheduled for Thursday at 3 PM."}

#     # 🧠 Use vector search + self-grading
#     rag = retrieve_docs(user_msg)
#     grade = self_grade(user_msg, rag["docs"])

#     if grade["relevance"] < 0.6 or grade["coverage"] < 0.6:
#         return {"response": "📭 Sorry, my knowledge base doesn't cover that topic."}

#     # ✅ Return top answer with citation
#     top = rag["docs"][0]
#     return {
#         "response": f"{top['content']}\n📚 Source: {top['source']}\n🔖 Topic: {top['metadata'].get('topic', 'N/A')}"
#     }

# from auth import router as auth_router
# app.include_router(auth_router)


# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from langchain.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from typing import List

# # -------- App setup --------
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------- Models --------
# class ChatInput(BaseModel):
#     message: str

# # -------- In-memory state --------
# feedback_score = 0.0
# task_list = []

# # -------- Feedback & Prompt --------
# def update_feedback(command: str):
#     global feedback_score
#     if command == "/good_answer":
#         feedback_score += 1
#     elif command == "/bad_answer":
#         feedback_score -= 1
#     feedback_score *= 0.5
#     return round(feedback_score, 2)

# def get_prompt():
#     if feedback_score < 0:
#         return "Be more concise and cite sources explicitly."
#     elif feedback_score > 0:
#         return "Maintain current style, user is satisfied."
#     else:
#         return "Respond normally."

# # -------- Task Manager --------
# def manage_tasks(action: str, task: dict = None):
#     if action == "add" and task:
#         task_list.append(task)
#         return f"Task added: {task['title']}"
#     elif action == "list":
#         return task_list
#     return "Invalid action."

# # -------- RAG Tools --------
# embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)

# def retrieve_docs(query: str):
#     results = vectorstore.similarity_search_with_score(query, k=3)
#     docs = []
#     for doc, score in results:
#         docs.append({
#             "content": doc.page_content,
#             "source": doc.metadata.get("source", "unknown"),
#             "metadata": doc.metadata
#         })
#     return {"docs": docs, "query": query}

# def self_grade(question: str, docs: List[dict]):
#     if not docs:
#         return {"relevance": 0.0, "coverage": 0.0}
#     relevance = 0.8 if any(q in docs[0]['content'].lower() for q in question.lower().split()) else 0.4
#     coverage = 0.7 if len(docs) > 1 else 0.5
#     return {"relevance": relevance, "coverage": coverage}

# # -------- Main Endpoint --------
# @app.post("/concierge/chat")
# async def chat(input: ChatInput):
#     user_msg = input.message.strip()

#     # Feedback
#     if user_msg in ["/good_answer", "/bad_answer"]:
#         new_score = update_feedback(user_msg)
#         return {"feedback_score": new_score, "prompt": get_prompt()}

#     # Task
#     if "schedule" in user_msg.lower():
#         manage_tasks("add", {
#             "title": "Demo Call",
#             "when": "Thursday 3 PM",
#             "description": "AI concierge demo"
#         })
#         return {"response": "✅ Demo call scheduled for Thursday at 3 PM."}

#     # RAG with self-grading
#     rag = retrieve_docs(user_msg)
#     grade = self_grade(user_msg, rag["docs"])

#     if grade["relevance"] < 0.6 or grade["coverage"] < 0.6:
#         return {"response": "📭 Sorry, my knowledge base doesn't cover that topic."}

#     top = rag["docs"][0]
#     return {
#         "response": f"{top['content']}\n📚 Source: {top['source']}\n🔖 Topic: {top['metadata'].get('topic', 'N/A')}"
#     }









from fastapi import FastAPI, Request, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List

# --------- FastAPI App Setup ---------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- JWT Setup ---------
JWT_SECRET = "supersecret"
JWT_ALGORITHM = "HS256"
security = HTTPBearer()

# --------- In-Memory Storage ---------
users = {}
feedback_score = 0.0
task_list = []

# --------- Models ---------
class ChatInput(BaseModel):
    message: str

class RegisterInput(BaseModel):
    username: str
    password: str

class LoginInput(BaseModel):
    username: str
    password: str

# --------- Auth Utils ---------

def verify_token_from_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# --------- Register/Login Endpoints ---------

@app.post("/register")
def register(input: RegisterInput):
    if input.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[input.username] = input.password
    return {"message": "✅ Registered successfully"}

@app.post("/login")
def login(input: LoginInput):
    if users.get(input.username) != input.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {
        "sub": input.username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token}

# --------- Feedback & Prompt ---------

def update_feedback(command: str):
    global feedback_score
    if command == "/good_answer":
        feedback_score += 1
    elif command == "/bad_answer":
        feedback_score -= 1
    feedback_score *= 0.5
    return round(feedback_score, 2)

def get_prompt():
    if feedback_score < 0:
        return "Be more concise and cite sources explicitly."
    elif feedback_score > 0:
        return "Maintain current style, user is satisfied."
    else:
        return "Respond normally."

# --------- Task Manager ---------

def manage_tasks(action: str, task: dict = None):
    if action == "add" and task:
        task_list.append(task)
        return f"Task added: {task['title']}"
    elif action == "list":
        return task_list
    return "Invalid action."

# --------- RAG Setup ---------
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)

def retrieve_docs(query: str):
    results = vectorstore.similarity_search_with_score(query, k=3)
    docs = []
    for doc, score in results:
        docs.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "metadata": doc.metadata
        })
    return {"docs": docs, "query": query}

def self_grade(question: str, docs: List[dict]):
    if not docs:
        return {"relevance": 0.0, "coverage": 0.0}
    relevance = 0.8 if any(q in docs[0]['content'].lower() for q in question.lower().split()) else 0.4
    coverage = 0.7 if len(docs) > 1 else 0.5
    return {"relevance": relevance, "coverage": coverage}

# --------- Chat Endpoint (Protected) ---------

@app.post("/concierge/chat")
async def chat(input: ChatInput, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    username = verify_token_from_token(token)
    user_msg = input.message.strip()

    if user_msg in ["/good_answer", "/bad_answer"]:
        new_score = update_feedback(user_msg)
        return {"feedback_score": new_score, "prompt": get_prompt()}

    if "schedule" in user_msg.lower():
        manage_tasks("add", {
            "title": "Demo Call",
            "when": "Thursday 3 PM",
            "description": "AI concierge demo"
        })
        return {"response": "✅ Demo call scheduled for Thursday at 3 PM."}

    if "what do i have" in user_msg.lower():
        tasks = manage_tasks("list")
        if not tasks:
            return {"response": "📭 No tasks scheduled."}
        return {
            "response": "\n".join([
                f"{i+1}. {t['title']} - {t['when']}\n   📋 {t['description']}"
                for i, t in enumerate(tasks)
            ])
        }

    rag = retrieve_docs(user_msg)
    grade = self_grade(user_msg, rag["docs"])

    if grade["relevance"] < 0.6 or grade["coverage"] < 0.6:
        return {"response": "📭 Sorry, my knowledge base doesn't cover that topic."}

    top = rag["docs"][0]
    return {
        "response": f"{top['content']}\n📚 Source: {top['source']}\n🔖 Topic: {top['metadata'].get('topic', 'N/A')}"
    }
