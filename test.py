import os
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from tqdm import tqdm


# 1. PDF faylni yuklash va parsing
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents


# 2. Chunklash
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = splitter.split_documents(documents)
    return docs


# 3. Savol-javob generatsiya qilish uchun prompt
prompt_template = """
Sen hujjat asosida savol va javob yaratadigan model san.

Hujjat bo‘lagi:
\"\"\"{context}\"\"\"

Shu hujjat asosida bitta savol va aniq javob yarat.

Format:
Q: Savol
A: Javob
"""

prompt = PromptTemplate(
    input_variables=["context"],
    template=prompt_template
)


# 4. Savol-javob generatsiya qilish
def generate_qa(docs, llm, output_file):
    with open(output_file, "w", encoding="utf-8") as fout:
        for doc in tqdm(docs):
            context = doc.page_content
            full_prompt = prompt.format(context=context)
            response = llm.invoke(full_prompt).strip()

            try:
                q_line, a_line = response.split("\n", 1)
                question = q_line.replace("Q:", "").strip()
                answer = a_line.replace("A:", "").strip()

                json_line = {
                    "messages": [
                        {"role": "system", "content": "Siz hujjatlar bo‘yicha yordamchisiz."},
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": answer}
                    ]
                }
                fout.write(json.dumps(json_line, ensure_ascii=False) + "\n")

            except Exception as e:
                print(f"Xatolik: {e}, javob: {response}")


# 5. Barchasini boshqarish
def pipeline(file_path, output_file):
    documents = load_pdf(file_path)
    docs = split_documents(documents)

    # Chat LLM ni ulaymiz (Deepseek lokal model)
    llm = ChatOpenAI(
        openai_api_base="http://localhost:8000/v1",
        openai_api_key="EMPTY",
        model_name="deepseek-chat",
        temperature=0.3
    )

    generate_qa(docs, llm, output_file)


# --- BOSHLA ---
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    pdf_file = "your_file.pdf"  # <-- o‘z faylingni joylashtir
    output_jsonl = "data/fine_tune_dataset.jsonl"
    pipeline(pdf_file, output_jsonl)
