import logging
from functools import lru_cache
from typing import Mapping, Optional

from hvac.exceptions import InvalidPath, Forbidden

from vault import config
from vault.client import get_client
from vault.exceptions import VaultClientImproperlyConfiguredError

logger = logging.getLogger(__name__)


def _validate_vault_config(
    auth_method: str,
    token: Optional[str] = None,
    role_id: Optional[str] = None,
    secret_id: Optional[str] = None,
) -> bool:
    if auth_method == "token":
        if not token:
            raise VaultClientImproperlyConfiguredError(
                "Missing variable VAULT_TOKEN. "
                "Cannot authenticate with vault using token."
            )
        return True

    if auth_method == "approle":
        if not role_id or not secret_id:
            raise VaultClientImproperlyConfiguredError(
                "Missing variables VAULT_ROLE_ID and/or VAULT_SECRET_ID. "
                "Cannot authenticate with vault using approle."
            )
        return True
    return False


@lru_cache
def _fetch_variables() -> Mapping[str, str]:
    try:
        _validate_vault_config(
            auth_method=config.VAULT_AUTH_METHOD,
            token=config.VAULT_TOKEN,
            role_id=config.VAULT_ROLE_ID,
            secret_id=config.VAULT_SECRET_ID,
        )
    except VaultClientImproperlyConfiguredError as e:
        logger.exception(e, exc_info=True)
        return dict()

    logger.debug("About to fetch credentials from vault.")
    if not (
        client := get_client(
            auth_method=config.VAULT_AUTH_METHOD,
            host=config.VAULT_HOST,
            token=config.VAULT_TOKEN,
            role_id=config.VAULT_ROLE_ID,
            secret_id=config.VAULT_SECRET_ID,
        )
    ):
        raise ConnectionError("Could not connect to vault.")

    logger.debug(f"Connected to vault with auth method {config.VAULT_AUTH_METHOD}.")
    try:
        response = client.secrets.kv.v2.read_secret(
            mount_point=config.VAULT_ENGINE_NAME,
            path=config.VAULT_PATH,
        )
    except InvalidPath:
        raise Exception(
            f"Your path ({config.VAULT_PATH}) has not been created yet "
            f"or there are no credentials in it."
        )
    except Forbidden:
        raise Exception(
            f"Your {config.VAULT_AUTH_METHOD} does not have access to the path "
            f"'{config.VAULT_PATH}'."
        )

    secrets = response["data"]["data"]
    logger.info(f"Fetched {len(secrets.keys())} secret(s) from vault.")
    return secrets


class Vault:
    _variables: Mapping[str, str] = dict()

    def __init__(self):
        self._variables = _fetch_variables()

    def __getitem__(self, key: str) -> Optional[str]:
        return self._variables[key]

    def get(self, key: str, default: str = None) -> Optional[str]:
        try:
            return self[key]
        except KeyError:
            return default
