import os
import glob
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize Global Instances
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistence File
DB_FILE = "./chroma_db/policies.json"
if not os.path.exists("./chroma_db"):
    os.makedirs("./chroma_db")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def index_policies(data_dir="./data"):
    """
    Reads all .txt files from data_dir and indexes them into a JSON file.
    """
    print(f"Indexing policies from {data_dir}...")
    
    files = glob.glob(os.path.join(data_dir, "*.txt"))
    if not files:
        print("No policy files found to index.")
        return

    db_data = []

    for file_path in files:
        file_name = os.path.basename(file_path)
        policy_name = file_name.replace(".txt", "").replace("_", " ").title()
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Generate embedding
        embedding = model.encode(content).tolist()
        
        db_data.append({
            "id": file_name,
            "text": content,
            "source": policy_name,
            "embedding": embedding
        })

    # Save to file
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_data, f)
        
    print(f"Indexed {len(db_data)} policies to {DB_FILE}.")

def retrieve_policies(query: str, k: int = 3):
    """
    Embeds the query and retrieves the top k similar policies using basic cosine similarity.
    """
    if not os.path.exists(DB_FILE):
        print("Database not found. Please index policies first.")
        return []
        
    with open(DB_FILE, "r", encoding="utf-8") as f:
        db_data = json.load(f)
        
    query_embedding = model.encode(query)
    
    scored_docs = []
    for doc in db_data:
        doc_embedding = np.array(doc["embedding"])
        score = cosine_similarity(query_embedding, doc_embedding)
        scored_docs.append((score, doc))
        
    # Sort by score desc
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    
    # Return top k
    top_k = scored_docs[:k]
    
    retrieved = []
    for score, doc in top_k:
        retrieved.append({
            "text": doc["text"],
            "source": doc["source"]
        })
            
    return retrieved

if __name__ == "__main__":
    index_policies()
    results = retrieve_policies("What is the leave policy?", k=1)
    print("Test Retrieval Result:", results)
