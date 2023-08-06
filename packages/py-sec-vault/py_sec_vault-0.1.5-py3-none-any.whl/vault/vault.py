import logging
from functools import lru_cache
from typing import Mapping, Optional, Tuple

from hvac import Client
from hvac.exceptions import InvalidPath, Forbidden

from . import config
from .client import get_client
from .exceptions import VaultClientImproperlyConfiguredError

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
    raise VaultClientImproperlyConfiguredError("Missing variable VAULT_AUTH_METHOD.")


class Vault:
    _variables: Mapping[str, str] = dict()
    _client: Optional[Client] = None

    def __init__(
        self,
        host: str = config.VAULT_HOST,
        engine_name: str = config.VAULT_ENGINE_NAME,
        path: str = config.VAULT_PATH,
        auth_method: str = config.VAULT_AUTH_METHOD,
        token: Optional[str] = config.VAULT_TOKEN,
        role_id: Optional[str] = config.VAULT_ROLE_ID,
        secret_id: Optional[str] = config.VAULT_SECRET_ID,
    ) -> None:
        try:
            _validate_vault_config(
                auth_method=auth_method,
                token=token,
                role_id=role_id,
                secret_id=secret_id,
            )
        except VaultClientImproperlyConfiguredError as e:
            logger.exception(e, exc_info=True)
            return

        self._client = get_client(
            auth_method=auth_method,
            host=host,
            token=token,
            role_id=role_id,
            secret_id=secret_id,
        )
        if not self._client:
            raise ConnectionError(
                "Could not connect to vault. Check your vault configuration."
            )

        logger.debug(f"Connected to vault with auth method {auth_method}.")
        self._variables = self._fetch_variables(
            engine_name=engine_name,
            vault_path=path,
        )

    def __getitem__(self, key: str) -> Optional[str]:
        return self._variables[key]

    @lru_cache
    def _fetch_variables(self, engine_name: str, vault_path: str) -> Mapping[str, str]:
        try:
            response = self._client.secrets.kv.v2.read_secret(
                mount_point=engine_name,
                path=vault_path,
            )
        except InvalidPath:
            raise Exception(
                f"Your path ({vault_path}) has not been created yet "
                f"or there are no credentials in it."
            )
        except Forbidden:
            raise Exception(
                f"Your client does not have access to the path '{vault_path}'."
            )

        variables = response["data"]["data"]
        logger.info(f"Fetched {len(variables.keys())} secret(s) from vault.")
        return variables

    def get(self, key: str, default: str = None) -> Optional[str]:
        try:
            return self[key]
        except KeyError:
            return default

    @property
    def keys(self) -> Tuple[str]:
        return tuple(self._variables.keys())
