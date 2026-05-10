import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load dataset
with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []

for item in catalog:

    text = f"""
    Assessment Name: {item.get('name', '')}

    Description:
    {item.get('description', '')}

    Categories:
    {', '.join(item.get('keys', []))}

    Job Levels:
    {', '.join(item.get('job_levels', []))}
    """

    texts.append(text)

# Generate embeddings
embeddings = model.encode(texts)

embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# Save
faiss.write_index(index, "faiss_index.index")

print("Embeddings created successfully.")