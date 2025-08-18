import os
from conjur import Client

class ConjurSecretProvider:
    def __init__(self):
        conjur_url = os.getenv("CONJUR_APPLIANCE_URL")
        conjur_account = os.getenv("CONJUR_ACCOUNT")
        conjur_login = os.getenv("CONJUR_AUTHN_LOGIN")
        conjur_api_key = os.getenv("CONJUR_AUTHN_API_KEY")

        if not all([conjur_url, conjur_account, conjur_login, conjur_api_key]):
            raise ValueError("Missing Conjur environment variables")

        # Initialize Conjur client
        self.client = Client.from_api_key(
            conjur_url=conjur_url,
            account=conjur_account,
            login_id=conjur_login,
            api_key=conjur_api_key,
        )

    def get_secret(self, variable_name: str) -> str:
        """
        Retrieve a secret value from Conjur.
        Example: provider.get_secret("prod/db/sqlserver/connection-string")
        """
        try:
            return self.client.get(variable_name)
        except Exception as e:
            raise RuntimeError(f"Error retrieving secret '{variable_name}': {e}")
