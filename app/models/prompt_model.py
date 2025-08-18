from pydantic import BaseModel

class PromptBase(BaseModel):
    id: int
    text: str
    description: str
