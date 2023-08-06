import os
from typing import Optional

from . import Vault


def from_env_or_vault(
    key: str,
    default: Optional[str] = None,
    vault: Optional[Vault] = None,
) -> Optional[str]:
    """
    Get a value first from the environment and if not found, from Vault. This function
    instantiates a Vault object (if not provided) resulting in a call to Vault to fetch;
    :param key: key to fetch from the environment or Vault
    :param default: default value to return if key is not found
    :param vault: Vault object to use to fetch the value, if not provided a new Vault object is instantiated
    :return: value from environment or Vault
    """
    return os.environ.get(key, (vault or Vault()).get(key, default or ""))


def from_vault_or_env(
    key: str,
    default: Optional[str] = None,
    vault: Optional[Vault] = None,
) -> Optional[str]:
    """
    Get a value first from Vault and if not found, from the environment. This function
    instantiates a Vault object (if not provided) resulting in a call to Vault to fetch;
    :param key: key to fetch from the environment or Vault
    :param default: default value to return if key is not found
    :param vault: Vault object to use to fetch the value, if not provided a new Vault object is instantiated
    :return: value from environment or Vault
    """
    return (vault or Vault()).get(key, default=os.environ.get(key, default or ""))


def from_vault(
    key: str,
    vault: Optional[Vault] = None,
) -> Optional[str]:
    """
    Get a value from Vault. This function instantiates a Vault object.
    Raises KeyError if key is not found in Vault.
    :param key: key to fetch from Vault
    :param vault: Vault object to use to fetch the value, if not provided a new Vault object is instantiated
    :return: value from Vault
    """
    return (vault or Vault())[key]
