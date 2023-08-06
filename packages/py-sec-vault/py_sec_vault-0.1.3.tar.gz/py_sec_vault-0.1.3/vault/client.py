from typing import Optional

from hvac import Client


def get_client(
    auth_method: str,
    host: str,
    token: Optional[str] = None,
    role_id: Optional[str] = None,
    secret_id: Optional[str] = None,
) -> Optional[Client]:
    if auth_method == "token":
        return Client(url=host, token=token)

    if auth_method == "approle":
        client = Client(url=host)
        client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id,
        )
        return client
