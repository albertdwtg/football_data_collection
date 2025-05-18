from google.cloud import secretmanager
from google.api_core.exceptions import NotFound
from utils.exceptions import SecretNotFoundError

def get_secret(project_id, secret_id, version_id="latest"):
    """
    Retrieves a secret from Google Cloud Secret Manager.

    Args:
        project_id (str): The GCP project ID.
        secret_id (str): The ID of the secret to retrieve.
        version_id (str): The version of the secret to retrieve. Defaults to "latest".

    Returns:
        str: The secret value.

    Raises:
        SecretNotFoundError: If the secret does not exist.
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": secret_name})
        return response.payload.data.decode("UTF-8")
    except NotFound as error:
        raise SecretNotFoundError(secret_id) from error
