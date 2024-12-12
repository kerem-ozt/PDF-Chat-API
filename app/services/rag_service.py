import os
from typing import List
from app.core.logger import logger
from app.utils.pdf_utils import preprocess_text

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from sentence_transformers import SentenceTransformer

model_name = "sentence-transformers/all-MiniLM-L6-v2"  
embedding_model = SentenceTransformer(model_name)

client = chromadb.Client(
    Settings(
        persist_directory="vectorstore"
    )
)

collection = client.get_or_create_collection(name="pdf_chunks")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start = end - overlap
        if start < 0:
            start = 0
        if start >= len(words):
            break
    return chunks

def embed_chunks(chunks: List[str]):
    embeddings = embedding_model.encode(chunks).tolist()
    return embeddings

def store_pdf_chunks(pdf_id: str, text: str):
    text = preprocess_text(text)
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    ids = [f"{pdf_id}_{i}" for i in range(len(chunks))]
    metadata = [{"pdf_id": pdf_id} for _ in chunks]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadata)
    logger.info(f"Stored {len(chunks)} chunks for PDF {pdf_id} in vector database.")

def retrieve_relevant_chunks(pdf_id: str, query: str, k: int = 3) -> List[str]:
    query_embedding = embedding_model.encode([query]).tolist()[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=k, where={"pdf_id": pdf_id})
    return results["documents"][0] if results and results["documents"] else []
