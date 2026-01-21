from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

pc = Pinecone(api_key="pcsk_2NpXNN_MV1ZNxYthPkWDmG8Vsv2MAtb6ouxUMuDMg6bfrJmCvXEpCbckaWCQ4jzYj6RxhX")

index = pc.Index("jarvis")

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "Diligent provides GRC SaaS software.",
    "Jarvis is an AI assistant for enterprises.",
    "Vector databases store embeddings."
]

vectors = []

text = "Sir's secret project codename is BluePhoenix42."

embedding = model.encode(text).tolist()
index.upsert([("secret1", embedding, {"text": text})])

print("Inserted test fact")

for i, text in enumerate(texts):
    emb = model.encode(text).tolist()
    vectors.append((str(i), emb, {"text": text}))

index.upsert(vectors)

print("Data stored successfully!")


query = "What does Diligent do?"
q_emb = model.encode(query).tolist()

result = index.query(vector=q_emb, top_k=1, include_metadata=True)

print(result.matches[0].metadata["text"])