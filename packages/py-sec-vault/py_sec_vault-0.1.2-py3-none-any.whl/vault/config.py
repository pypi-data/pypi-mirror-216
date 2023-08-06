import os

VAULT_HOST = os.environ.get("VAULT_HOST", "http://localhost:8200/")
VAULT_AUTH_METHOD = os.environ.get("VAULT_AUTH_METHOD", "token")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN")
VAULT_ROLE_ID = os.environ.get("VAULT_ROLE_ID")
VAULT_SECRET_ID = os.environ.get("VAULT_SECRET_ID")
VAULT_ENGINE_NAME = os.environ.get("VAULT_ENGINE_NAME")
VAULT_PATH = os.environ.get("VAULT_PATH")
