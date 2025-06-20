import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os, pickle

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

class RAGEngine:
    def __init__(self, index_path="index/index.faiss", store_path="index/store.pkl"):
        self.index_path = index_path
        self.store_path = store_path
        self.index = None
        self.text_chunks = []
        self.load()

    def load(self):
        if os.path.exists(self.index_path) and os.path.exists(self.store_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.store_path, "rb") as f:
                self.text_chunks = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(384)

    def add_texts(self, texts: list[str]):
        embeddings = model.encode(texts)
        self.index.add(np.array(embeddings).astype("float32"))
        self.text_chunks.extend(texts)
        faiss.write_index(self.index, self.index_path)
        with open(self.store_path, "wb") as f:
            pickle.dump(self.text_chunks, f)

    def search(self, query, top_k=3):
        query_vector = model.encode([query]).astype("float32")
        D, I = self.index.search(query_vector, top_k)
        return [self.text_chunks[i] for i in I[0] if i < len(self.text_chunks)]
