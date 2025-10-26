import os
from pathlib import Path
from typing import List, Dict, Tuple

from langchain_community.vectorstores import FAISS
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage

from app.core.config import settings

k_default = int(os.environ.get("K_DEFAULT"))

def embeddings():
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)

def load_faiss() -> FAISS:
    index_dir = Path(settings.index_path)
    if not index_dir.exists():
        raise FileNotFoundError(f"FAISS index not found at {index_dir}. Сначала вызови /ingest.")
    return FAISS.load_local(
        folder_path=str(index_dir),
        embeddings=embeddings(),
        allow_dangerous_deserialization=True,
    )

def _llm() -> ChatHuggingFace:
    endpoint = HuggingFaceEndpoint(
        repo_id=settings.hf_model_id,
        task="conversational",
        temperature=0.2,
        max_new_tokens=512,
        huggingfacehub_api_token=settings.hf_token,
    )
    return ChatHuggingFace(llm=endpoint)

def format_context(docs: List) -> str:
    lines = []
    for d in docs:
        src = d.metadata.get("source", "unknown")

        page_meta = d.metadata.get("page", "unknown")
        if isinstance(page_meta, int):
            page = page_meta + 1
        else:
            try:
                page = int(page_meta) + 1
            except Exception:
                page = page_meta

        basename = Path(src).name if src != "unknown" else src
        lines.append(f"[doc: {basename}; page: {page}]\n{d.page_content}")
    return "\n\n---\n\n".join(lines)

def build_prompt(question: str, context: str) -> str:
    return (
        "Ты — помощник по PDF. Отвечай ТОЛЬКО на основе контекста.\n"
        "Если в контексте нет ответа, честно скажи об этом.\n\n"
        f"ВОПРОС:\n{question}\n\n"
        f"КОНТЕКСТ:\n{context}\n\n"
        "Требования к ответу:\n"
        "- Кратко и структурированно.\n"
        "- В конце, если ты нашел ответ в контексте, добавь список цитат в формате: [doc: <имя файла>, p.<номер страницы>].\n"

    )

def ask(question: str, k: int = k_default) -> Dict:
    db = load_faiss()
    docs = db.similarity_search(question, k=k)

    context = format_context(docs)
    prompt = build_prompt(question, context)

    llm = _llm()
    answer_msg = llm.invoke([HumanMessage(content=prompt)])
    answer_text = answer_msg.content if hasattr(answer_msg, "content") else str(answer_msg)

    cites: List[Tuple[str, int]] = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", -1)
        cites.append((src, page))

    uniq: List[Tuple[str, int]] = []
    seen = set()
    for c in cites:
        if c not in seen:
            uniq.append(c)
            seen.add(c)

    return {
        "answer": answer_text,
        "citations": [{"source": s, "page": int(p) if isinstance(p, int) else p} for (s, p) in uniq],
        "used_k": k,
    }