from typing import Optional, List
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str
    hf_model_id: str
    embedding_model: str

class IngestResponse(BaseModel):
    status: str
    filename: str
    saved_to: str
    chunks_added: int
    index_path: str

class AskRequest(BaseModel):
    question: str
    k: Optional[int] = Field(4, ge=1, le=10)

class Citation(BaseModel):
    source: str
    page: int | str

class AskResponse(BaseModel):
    status: str
    answer: str
    citations: List[Citation]
    used_k: int

class MaintenanceResponse(BaseModel):
    status: str
    action: str
    removed_files: list[str] | None = None
