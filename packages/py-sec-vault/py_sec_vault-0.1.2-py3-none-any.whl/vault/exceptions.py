class VaultClientImproperlyConfiguredError(Exception):
    def __init__(self, message: str = "Vault client is improperly configured."):
        self.message = message
        super().__init__(self.message)
