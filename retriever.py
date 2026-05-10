import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load catalog
with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load index
index = faiss.read_index("faiss_index.index")


def retrieve_assessments(query, top_k=10):

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        results.append(catalog[idx])

    return results