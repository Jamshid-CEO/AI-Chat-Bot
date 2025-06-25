import faiss
from sentence_transformers import SentenceTransformer
from loader import load_knowledge_base

class RAGEngine:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.texts = []
        self.embeddings = []
        self.index = None

    def add_document(self, file_path):
        from loader import load_single_file
        new_text = load_single_file(file_path)
        if new_text:
            self.texts.append(new_text)
            embedding = self.model.encode([new_text])
            self.embeddings.append(embedding[0])

            if self.index is None:
                self.index = faiss.IndexFlatL2(len(embedding[0]))
            self.index.add(embedding)

    def retrieve(self, query, top_k=3):
        if self.index is None:
            return []
        query_embedding = self.model.encode([query])
        D, I = self.index.search(query_embedding, top_k)
        return [self.texts[i] for i in I[0]]
