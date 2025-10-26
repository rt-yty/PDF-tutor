from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings
from app.models.schemas import IngestResponse
from app.services.ingest import save_upload, ingest_pdf_file

router = APIRouter(tags=["ingest"])

@router.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Пожалуйста, загрузите PDF-файл.")
    content = await file.read()
    saved_path = save_upload(content, file.filename)
    try:
        n_chunks = ingest_pdf_file(saved_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingest error: {e}")
    return IngestResponse(
        status="ok",
        filename=file.filename,
        saved_to=str(saved_path),
        chunks_added=n_chunks,
        index_path=settings.index_path,
    )
