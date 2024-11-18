from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Key Vault
KEY_VAULT_URI = f"https://b00858494keyvault.vault.azure.net/"

# Initialise Azure Key Vault Client
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URI, credential=credential)

secret = client.get_secret("testsecret")
secret_value = secret.value
print("Secret: " + secret_value)