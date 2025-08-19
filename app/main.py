# app/main.py
import os
from fastapi import FastAPI
from app.api import prompts_controller
from app.config.conjur_client import ConjurSecretProvider

def fetch_and_set_conjur_secrets():
    """
    Fetch required secrets from Conjur and set them into environment variables
    for the rest of the app to use.
    """
    provider = ConjurSecretProvider()

    # Example: fetch DB connection string from Conjur
    db_conn_str = provider.get_secret("prod/db/sqlserver/connection-string")

    # Set in environment for database.py to use
    os.environ["DB_CONNECTION_STRING"] = db_conn_str


# Initialize FastAPI app
app = FastAPI(title="FastAPI + Conjur Example")

# Load secrets once during startup
# @app.on_event("startup")
# def startup_event():
#     fetch_and_set_conjur_secrets()


# Register controllers/routers
app.include_router(prompts_controller.router, prefix="/api", tags=["Prompts"])
