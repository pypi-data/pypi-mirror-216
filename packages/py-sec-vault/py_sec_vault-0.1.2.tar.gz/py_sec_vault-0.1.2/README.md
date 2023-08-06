# PySecVault
Hashicorp Vault implementation in python software


## Pre-requisites
To use this software, you need to have a running instance of Hashicorp Vault.
You can find the installation instructions [here](https://learn.hashicorp.com/vault/getting-started/install).

Alternatively, you can use the docker image provided by Hashicorp [here](https://hub.docker.com/_/vault/).

```bash
docker run --cap-add=IPC_LOCK \
  -e 'VAULT_LOCAL_CONFIG={"storage": {"file": {"path": "/vault/file"}}, "listener": [{"tcp": { "address": "0.0.0.0:8200", "tls_disable": true}}], "default_lease_ttl": "168h", "max_lease_ttl": "720h", "ui": true}' \
  -p 8200:8200 vault server
```

After this command, you can access the vault UI at http://localhost:8200
and follow the instructions to initialize the vault.

## Installation

```bash
pip install py-sec-vault
```

After this you should set environment variables to connect to the vault instance.

```
export VAULT_HOST=http://localhost:8200/
export VAULT_AUTH_METHOD=approle|token
export VAULT_ENGINE_NAME=<my_engine_name>
export VAULT_ROLE_ID=<my_vault_id>
export VAULT_SECRET_ID=<my_vauld_secret>
export VAULT_PATH=<my_vault_path>
```

## Usage

```python
from vault import Vault

vault = Vault()

# Retrieving a secret from the vault, or None if not found
my_optional_secret = vault.get("MY_SECRET")

# Retrieving a secret from the vault (and raising an exception if not found)
my_secret = vault["MY_SECRET"]
```

## Usage with environment variables
```python
from vault import from_env_or_vault, from_vault

# NB: These functions will instantiate a Vault object and retrieve the secret from the vault
# resulting in a performance penalty if used in a loop; in that case, instantiate a Vault object.

# Retrieving a secret from the vault or environment variable or using a default value
from_env_or_vault("DB_PASSWORD", default="admin")

# Retrieving a secret from the vault (and raising an exception if not found)
from_vault("API_TOKEN")
```

## Next steps
- [ ] Make sure the vault is not initialized every time, but only when needed
- [ ] On init load multiple paths/engines
- [ ] Add support for other auth methods
- [ ] Phase out the use of hvac and use requests instead
- [ ] Implementation of from_vault_or_env
