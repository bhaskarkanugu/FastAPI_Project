import os
import pymssql # Import pymssql
from fastapi import APIRouter, Depends, HTTPException
from app.config.database import get_db
from app.models.prompt_model import PromptBase
from app.repositories.prompt_repository import PromptRepository
from app.services.prompt_service import PromptService

router = APIRouter()

@router.get("/prompts/{id}", response_model=PromptBase)
def get_prompt(id: int, conn: pymssql.Connection = Depends(get_db)):
    """
    Retrieves a prompt by ID from the database using the
    pymssql connection provided by the get_db dependency.
    """
    repo = PromptRepository(conn)
    service = PromptService(repo)

    try:
        return service.get_prompt(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
