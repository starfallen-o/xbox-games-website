from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

# Key Vault
KEY_VAULT_URI = f"https://b00858494keyvault.vault.azure.net/"

# Initialize Azure Key Vault Client
credential = DefaultAzureCredential()
vault_client = SecretClient(vault_url=KEY_VAULT_URI, credential=credential)

# Initialize CosmosDB Client
COSMOSDB_ENDPOINT = vault_client.get_secret("CosmosDBEndpoint").value
COSMOSDB_KEY = vault_client.get_secret("CosmosDBKey").value
DATABASE_NAME = "gamesDB"
GAMES_CONTAINER = "games"

cosmos_client = CosmosClient(COSMOSDB_ENDPOINT, COSMOSDB_KEY)
database = cosmos_client.get_database_client(DATABASE_NAME)
games_container = database.get_container_client(GAMES_CONTAINER)

# Intialize Blob Storage Client
BLOB_CONNECTION_STRING = vault_client.get_secret("BlobConnectionString").value
BLOB_CONTAINER_NAME = "game-media"

blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)