import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from unittest.mock import patch, MagicMock
from app.api.prompts_controller import router
from app.models.prompt_model import PromptBase

app = FastAPI()
app.include_router(router)

@pytest.fixture
def client():
    return TestClient(app)

def test_get_prompt_success(client):
    prompt_data = {"id": 1, "title": "Test Prompt", "content": "Sample content"}
    with patch("app.services.prompt_service.PromptService.get_prompt", return_value=prompt_data):
        response = client.get("/prompts/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == prompt_data

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
    # Simulate a database error by raising an exception in PromptRepository
    with patch("app.repositories.prompt_repository.PromptRepository.__init__", side_effect=Exception("DB Error")):
        response = client.get("/prompts/1")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR or response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_prompt_service_exception(client):
    # Simulate an unexpected exception in the service
    with patch("app.services.prompt_service.PromptService.get_prompt", side_effect=Exception("Unexpected error")):
        response = client.get("/prompts/1")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR or response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY