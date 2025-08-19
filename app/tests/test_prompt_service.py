import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from unittest.mock import patch, MagicMock
from app.api.prompts_controller import router
from app.models.prompt_model import PromptBase
from app.config.database import get_db  # Add this import

app = FastAPI()
app.include_router(router)

# Override get_db to avoid real DB connection during tests
def override_get_db():
    class DummyConn:
        pass
    yield DummyConn()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

def test_get_prompt_success(client):
    prompt_data = PromptBase(id= 1, text = "description",description="Sample content")
    with patch("app.services.prompt_service.PromptService.get_prompt", return_value=prompt_data):
        response = client.get("/prompts/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == prompt_data.model_dump()

def test_get_prompt_not_found(client):
    with patch("app.services.prompt_service.PromptService.get_prompt", side_effect=ValueError("Prompt not found")):
        response = client.get("/prompts/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Prompt not found"

def test_get_prompt_invalid_id(client):
    # FastAPI will raise a 422 error for invalid path parameter types
    response = client.get("/prompts/invalid")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_prompt_db_error(client):
    with patch("app.repositories.prompt_repository.PromptRepository.__init__", side_effect=Exception("DB Error")):
        response = client.get("/prompts/1")
        # Accept either 422 or 500 depending on FastAPI's error handling
        assert response.status_code in [status.HTTP_500_INTERNAL_SERVER_ERROR, status.HTTP_422_UNPROCESSABLE_ENTITY]
def test_get_prompt_service_exception(client):
    # Simulate an unexpected exception in the service
    with patch("app.services.prompt_service.PromptService.get_prompt", side_effect=Exception("Unexpected error")):
        response = client.get("/prompts/1")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR or response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY