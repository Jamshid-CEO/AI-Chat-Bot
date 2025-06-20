import os
import chardet
from fastapi import FastAPI, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA

app = FastAPI()

# Embedding modeli
embedding_model = HuggingFaceEmbeddings(
    model_name="moka-ai/m3e-small"
)

vectorstore = None

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    global vectorstore

    contents = await file.read()
    file_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(contents)

    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        # Har qanday encoding aniqlash
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            print(f"Encoding aniqlandi: {encoding}")

        loader = TextLoader(file_path, encoding=encoding)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    else:
        return {"error": "Unsupported file type"}

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(docs, embedding_model)

    return {"message": "File successfully uploaded and embedded."}

@app.get("/chat/")
async def chat(question: str):
    global vectorstore

    llm = ChatOllama(
        model="deepseek-r1:1.5b",
        temperature=0
    )

    if vectorstore:
        retriever = vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )
        answer = qa_chain.run(question)
    else:
        answer = llm.invoke(question)

    return {"answer": answer}
