from langchain.vectorstores import chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders import PyPDFLoader
import os

CHROMA_PATH = "embeddings"

def load_documents():
    loader = PyPDFLoader("documents/physics_unit3.pdf")
    return loader.load()

def save_to_vectorstore():
    docs = load_documents()
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = chroma.from_documents(documents=docs, embedding=embedding, persist_directory=CHROMA_PATH)
    vectordb.persist()
    print("✅ Notes saved to vector DB!")

def  load_vectorstore():
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
    return vectordb
