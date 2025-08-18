from typing import Optional
import pyodbc

class PromptRepository:
    def __init__(self, conn: pyodbc.Connection):
        self.conn = conn

    def get_prompt_by_id(self, prompt_id: int) -> Optional[dict]:
        cursor = self.conn.cursor()
        query = "SELECT id, text, description FROM prompts WHERE id = ?"
        cursor.execute(query, (prompt_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return {"id": row[0], "text": row[1], "description": row[2]}
        return None
