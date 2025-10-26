import os
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings

chank_size = int(os.environ.get("CHUNK_SIZE"))
chunk_overlap = int(os.environ.get("CHUNK_OVERLAP"))

def ensure_dirs() -> None:
    Path(settings.data_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.index_path).parent.mkdir(parents=True, exist_ok=True)

def save_upload(bytes_content: bytes, filename: str) -> Path:
    ensure_dirs()
    safe_name = filename.replace("/", "_").replace("\\", "_")
    out_path = Path(settings.data_dir) / safe_name
    out_path.write_bytes(bytes_content)
    return out_path

def load_pdf(path: Path):
    loader = PyPDFLoader(str(path))
    return loader.load()

def split_docs(docs) -> List:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chank_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    return splitter.split_documents(docs)

def embeddings():
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)

def build_or_update_faiss(chunks) -> None:
    ensure_dirs()
    index_dir = Path(settings.index_path)
    embed = embeddings()

    if index_dir.exists():
        db = FAISS.load_local(
            folder_path=str(index_dir),
            embeddings=embed,
            allow_dangerous_deserialization=True,
        )
        db.add_documents(chunks)
        db.save_local(str(index_dir))
    else:
        db = FAISS.from_documents(chunks, embed)
        db.save_local(str(index_dir))

def ingest_pdf_file(path: Path) -> int:
    docs = load_pdf(path)
    chunks = split_docs(docs)
    build_or_update_faiss(chunks)
    return len(chunks)
