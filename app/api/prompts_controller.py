from fastapi import APIRouter, Depends, HTTPException
from app.config.database import get_db
from app.repositories.prompt_repository import PromptRepository
from app.services.prompt_service import PromptService
from app.models.prompt_model import PromptBase
import pyodbc

router = APIRouter()

@router.get("/prompts/{id}", response_model=PromptBase)
def get_prompt(id: int, conn: pyodbc.Connection = Depends(get_db)):
    repo = PromptRepository(conn)
    service = PromptService(repo)

    try:
        return service.get_prompt(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
