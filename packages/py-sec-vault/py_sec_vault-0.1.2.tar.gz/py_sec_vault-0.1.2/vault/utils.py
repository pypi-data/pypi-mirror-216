import os
from typing import Optional

from vault import Vault


def from_env_or_vault(
    key: str,
    default: Optional[str] = None,
) -> Optional[str]:
    """
    Get a value from the environment or from Vault. This function
    instantiates a Vault object resulting in a call to Vault to fetch;
    :param key: key to fetch from the environment or Vault
    :param default: default value to return if key is not found
    :return: value from environment or Vault
    """
    return os.environ.get(key, Vault().get(key, default or ""))


def from_vault(key: str) -> Optional[str]:
    """
    Get a value from Vault. This function instantiates a Vault object.
    Raises KeyError if key is not found in Vault.
    :param key: key to fetch from Vault
    :return: value from Vault
    """
    return Vault()[key]
