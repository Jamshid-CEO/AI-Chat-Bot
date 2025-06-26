import faiss
import numpy as np
import os
import tiktoken
from loader import load_knowledge_base
from embed import get_embedding

class RAGEngine:
    def __init__(self, knowledge_folder="knowledge_base", embedding_folder="knowledge_embedding"):
        self.docs = []
        self.index = None
        self.knowledge_folder = knowledge_folder
        self.embedding_folder = embedding_folder
        os.makedirs(self.embedding_folder, exist_ok=True)
        self.tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")
        self._load_all_documents()

    def _split_text(self, text, max_tokens=700):
        tokens = self.tokenizer.encode(text)
        chunks = []
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i:i + max_tokens]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
        return chunks

    def _embedding_exists(self, filename_prefix):
        return any(f.startswith(filename_prefix) and f.endswith(".npy") for f in os.listdir(self.embedding_folder))

    def _load_embeddings_from_disk(self, filename_prefix):
        for f in sorted(os.listdir(self.embedding_folder)):
            if f.startswith(filename_prefix) and f.endswith(".npy"):
                emb = np.load(os.path.join(self.embedding_folder, f))
                with open(os.path.join(self.embedding_folder, f.replace(".npy", ".txt")), 'r', encoding='utf-8') as txt_file:
                    chunk_text = txt_file.read()

                if self.index is None:
                    self.index = faiss.IndexFlatL2(len(emb))
                self.index.add(np.array([emb]))
                self.docs.append(chunk_text)

    def _save_embedding_to_disk(self, prefix, index, emb, chunk_text):
        emb_path = os.path.join(self.embedding_folder, f"{prefix}_chunk_{index}.npy")
        txt_path = os.path.join(self.embedding_folder, f"{prefix}_chunk_{index}.txt")
        np.save(emb_path, np.array(emb).astype("float32"))
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(chunk_text)

    def add_document(self, file_path: str):
        filename = os.path.basename(file_path)
        file_id = os.path.splitext(filename)[0]

        if self._embedding_exists(file_id):
            self._load_embeddings_from_disk(file_id)
            print(f"✅ '{file_id}' fayl embeddinglari diska yuklangan.")
            return

        text = load_knowledge_base(file_path)
        chunks = self._split_text(text)

        for idx, chunk in enumerate(chunks):
            try:
                emb = get_embedding(chunk)
                emb_array = np.array(emb).astype("float32")

                if self.index is None:
                    self.index = faiss.IndexFlatL2(len(emb_array))
                self.index.add(np.array([emb_array]))
                self.docs.append(chunk)

                self._save_embedding_to_disk(file_id, idx, emb_array, chunk)
            except Exception as e:
                print(f"⚠️ Embedding xatolik: {file_id} - {e}")

    def _load_all_documents(self):
        for filename in os.listdir(self.knowledge_folder):
            file_path = os.path.join(self.knowledge_folder, filename)
            if os.path.isfile(file_path):
                try:
                    self.add_document(file_path)
                except Exception as e:
                    print(f"⚠️ Faylni yuklashda xatolik: {filename} - {e}")

    def retrieve(self, query: str, top_k=3):
        if not self.index or not self.docs:
            return []
        q_emb = get_embedding(query)
        D, I = self.index.search(np.array([q_emb]).astype("float32"), top_k)
        return [self.docs[i] for i in I[0] if i < len(self.docs)]
