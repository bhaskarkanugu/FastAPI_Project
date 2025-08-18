# app/config/settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Prompt API"
    APP_ENV: str = "development"  # development, staging, production

    # Database
    CONJUR_DB_CONN_STRING: str  # retrieved from Conjur and injected into env

    # Conjur
    CONJUR_APPLIANCE_URL: str
    CONJUR_ACCOUNT: str
    CONJUR_AUTHN_LOGIN: str
    CONJUR_AUTHN_API_KEY: str
    CONJUR_VERIFY_SSL: bool = True

    class Config:
        env_file = ".env"  # useful for local development

# Singleton settings object
settings = Settings()
