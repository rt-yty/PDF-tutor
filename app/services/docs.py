from pathlib import Path
from typing import List

from app.services.qa import load_faiss

def list_documents() -> List[str]:
    try:
        db = load_faiss()
    except FileNotFoundError:
        return []

    sources = set()
    for doc in db.docstore._dict.values():
        src = doc.metadata.get("source")
        if src:
            sources.add(Path(src).name)
    return sorted(sources)