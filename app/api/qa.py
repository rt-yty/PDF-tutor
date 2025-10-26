# app/api/qa.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import AskRequest, AskResponse
from app.services.qa import ask as ask_service

router = APIRouter(tags=["qa"])

@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    try:
        result = ask_service(req.question, k=req.k or 4)
        return {"status": "ok", **result}
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ask error: {e}")
