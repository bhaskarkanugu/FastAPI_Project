from typing import Optional
import pymssql # Import pymssql

class PromptRepository:
    def __init__(self, conn: pymssql.Connection):
        """
        Initializes the repository with a pymssql database connection.
        """
        self.conn = conn

    def get_prompt_by_id(self, prompt_id: int) -> Optional[dict]:
        """
        Fetches a single prompt by its ID from the database.
        """
        # Using a 'with' statement ensures the cursor is automatically closed.
        with self.conn.cursor() as cursor:
            # Note: pymssql uses a different placeholder (%d or %s) than pyodbc (?)
            query = "SELECT id, text, description FROM prompts WHERE id = %d"
            cursor.execute(query, (prompt_id,))
            row = cursor.fetchone()

        if row:
            # Assuming the connection was created with as_dict=True,
            # the row is a dictionary, making column access more readable.
            return {"id": row['id'], "text": row['text'], "description": row['description']}
        return None
