import csv
import os
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from app.rag_data import index_policies
from app.rag_core import answer_question

app = FastAPI(title="NovaTech Policy Chatbot")

# Setup Logging
LOG_FILE = "logs/queries.csv"

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Initialize log file with header if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "question", "answer", "sources", "role", "language"])

class AskRequest(BaseModel):
    question: str
    show_sources: bool = True
    language: Optional[str] = "English"
    role: Optional[str] = "Employee"

@app.on_event("startup")
async def startup_event():
    # Index policies on startup
    # We run this synchronously as it's critical for the app to function
    index_policies()

def log_interaction(question, answer, sources, role, language):
    try:
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                question,
                answer,
                "|".join(sources),
                role,
                language
            ])
    except Exception as e:
        print(f"Error logging interaction: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ask")
async def ask(request: AskRequest, background_tasks: BackgroundTasks):
    try:
        # Get answer from RAG
        # Note: If language is not English, we might want to instruct LLM to translate,
        # but for now we just pass it to logging as per req.
        # Although, modifying prompt to respect language would be better:
        
        final_question = request.question
        if request.language and request.language.lower() != "english":
             final_question += f" (Please answer in {request.language} language)"

        result = answer_question(final_question)
        answer = result["answer"]
        sources = result["sources"]
        
        # Log in background
        background_tasks.add_task(
            log_interaction, 
            request.question, 
            answer, 
            sources, 
            request.role, 
            request.language
        )
        
        return {
            "answer": answer,
            "sources": sources if request.show_sources else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount frontend
# We check if frontend dir exists to avoid errors during initial creation steps
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
else:
    print("Frontend directory not found. Static files will not be served.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
