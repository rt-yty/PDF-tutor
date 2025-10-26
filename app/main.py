from fastapi import FastAPI

from app.core.config import settings
from app.models.schemas import HealthResponse
from app.api.ingest import router as ingest_router
from app.api.qa import router as qa_router
from app.api.maintenance import router as maintenance_router
from app.api.docs import router as docs_router

app = FastAPI(title="PDF-Tutor")

@app.get("/health", response_model=HealthResponse, tags=["health"])
def health():
    return HealthResponse(
        status="ok",
        hf_model_id=settings.hf_model_id,
        embedding_model=settings.embedding_model,
    )

# Подключаем роутеры
app.include_router(ingest_router)
app.include_router(docs_router)
app.include_router(qa_router)
app.include_router(maintenance_router)
