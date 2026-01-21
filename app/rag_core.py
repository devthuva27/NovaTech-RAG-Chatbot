from app.rag_data import retrieve_policies
from app.groq_llm import generate_answer

TEMPLATE = """You are NovaTech Inc.'s policy assistant. Answer ONLY from these policies:

[Context]
{POLICY_BLOCKS}

Question: {QUESTION}

Answer clearly, reference policy names."""

def answer_question(question: str, k: int = 3):
    """
    Orchestrates the RAG flow: Retrieve -> Prompt -> Generate.
    """
    # 1. Retrieve
    # We retrieve top 3 documents
    retrieved_docs = retrieve_policies(question, k=k)
    
    # 2. Format Context
    if not retrieved_docs:
        return {
            "answer": "I couldn't find any relevant policies to answer your question. Please try asking differently.",
            "sources": []
        }

    policy_blocks = ""
    sources = []
    seen_sources = set()

    for doc in retrieved_docs:
        source = doc['source']
        text = doc['text']
        policy_blocks += f"-- Policy: {source} --\n{text}\n\n"
        
        if source not in seen_sources:
            sources.append(source)
            seen_sources.add(source)

    # 3. Construct Prompt
    prompt = TEMPLATE.format(POLICY_BLOCKS=policy_blocks, QUESTION=question)
    
    # 4. Generate
    answer = generate_answer(prompt)
    
    return {
        "answer": answer,
        "sources": sources
    }
