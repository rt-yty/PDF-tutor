from typing import List

from fastapi import APIRouter
from app.services.docs import list_documents

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("", response_model=List[str])
def list_docs() -> List[str]:
    return list_documents()