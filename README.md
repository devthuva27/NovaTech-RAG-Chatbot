# NovaTech Policy Chatbot

A production-ready RAG (Retrieval-Augmented Generation) chatbot for NovaTech policies, utilizing **FastAPI**, **Sentence Transformers**, and the **Groq API** (Llama 3.3 70B).

## Features
- **RAG Architecture**: Retrieves relevant policy sections before answering.
- **Local Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2`.
- **Vector Store**: Lightweight local JSON vector store (no complex dependencies).
- **LLM**: `Llama 3.3 70B Versatile` via Groq for high-quality inference.
- **Frontend**: Clean, responsive HTML/JS UI with role/language options.
- **Logging**: All queries logged to `logs/queries.csv`.

## Project Structure
```text
novatech-policy-chatbot/
├── data/              # Policy text files
├── app/               # Backend modules
│   ├── api.py         # FastAPI app
│   ├── rag_core.py    # RAG logic
│   ├── rag_data.py    # Vector Store & Embeddings
│   └── groq_llm.py    # LLM Client
├── frontend/          # Web UI
├── chroma_db/         # Vector Store (JSON file)
├── logs/              # Usage logs
└── requirements.txt   # Dependencies
```

## Setup & Run

### 1. Prerequisites
- Python 3.9+
- A Groq API Key (Get one at https://console.groq.com)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Configuration
Open `.env` and paste your API Key:
```
GROQ_API_KEY=gsk_...
```

### 4. Run Server
```bash
uvicorn app.api:app --reload
```
*Wait for "Indexed 10 policies successfully" message on first run.*

### 5. Usage
- Open browser to `http://localhost:8000`
- Ask questions like:
    - "What is the policy on remote work?"
    - "Can I carry over my annual leave?"
    - "What are the core hours?"

## Troubleshooting
- **Rate Limit**: If Groq API 429 errors occur, the app waits and retries.
- **Missing Data**: Ensure `data/` folder has `.txt` files.
- **Embeddings**: First run downloads the embedding model (approx 50MB~).
