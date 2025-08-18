from app.models.prompt_model import PromptBase
from app.repositories.prompt_repository import PromptRepository

class PromptService:
    def __init__(self, repo: PromptRepository):
        self.repo = repo

    def get_prompt(self, prompt_id: int) -> PromptBase:
        """
        Business logic for retrieving a prompt by ID.
        Converts DB result into a Pydantic model.
        """
        data = self.repo.get_prompt_by_id(prompt_id)

        if not data:
            raise ValueError(f"Prompt with id {prompt_id} not found")

        # Convert dict -> Pydantic model
        return PromptBase(**data)


