import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag import faiss_index

def test_retriever_returns_pdf_content():
    query = "What is PCA?"
    retriever = faiss_index.as_retriever()
    docs = retriever.get_relevant_documents(query)
    for doc in docs:
        print("Retrieved:", doc.page_content[:200])
    assert any("Principal Component Analysis" in doc.page_content for doc in docs), "RAG did not retrieve expected content from PDFs"

def test_retriever_returns_anything():
    query = "Some random query"
    retriever = faiss_index.as_retriever()
    docs = retriever.get_relevant_documents(query)
    assert len(docs) > 0, "RAG did not return any documents"