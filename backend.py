from fastapi import FastAPI
from pydantic import BaseModel
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import requests

app = FastAPI()

# --- Pinecone ---
pc = Pinecone(api_key="pcsk_2NpXNN_MV1ZNxYthPkWDmG8Vsv2MAtb6ouxUMuDMg6bfrJmCvXEpCbckaWCQ4jzYj6RxhX")
index = pc.Index("jarvis")

# --- Embedding model ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Ollama ---
OLLAMA_URL = "http://localhost:11434/api/generate"

class Query(BaseModel):
    question: str

def query_llm(prompt):
    res = requests.post(OLLAMA_URL, json={
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    })
    return res.json()["response"]

@app.post("/chat")
def chat(q: Query):
    embedding = model.encode(q.question).tolist()

    result = index.query(
        vector=embedding,
        top_k=3,
        include_metadata=True
    )

    context = " ".join(
        [m.metadata["text"] for m in result.matches]
    )

    prompt = f"""
You are Jarvis, a professional AI assistant.

Rules:
- The user is always called "Sir".
- You are called "Jarvis".
- Never call the user Jarvis.
- Be polite, concise, and professional.

Context:
{context}

User question:
{q.question}

Answer as Jarvis speaking to Sir.
"""

    answer = query_llm(prompt)

    return {"answer": answer}
