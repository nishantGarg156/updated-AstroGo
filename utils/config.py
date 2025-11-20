# utils/config.py

#BASE_URL = "https://api.vrgo.test.xp.irdeto.com"
import uuid


BASE_URL = "https://api.vrgo.load.xp.irdeto.com"

Logging = True

PLATFORM = "WEB"

 # generate random device_id


def log(string: str):
    if Logging:
        print(f"[LOG] {string}")


def get_headers(platform: str, x_api_key: str = None, device_id: str = None, token: str = None) -> dict:
    """
    Returns a dictionary of headers for API requests.

    Args:
        platform (str): Platform identifier.
        x_api_key (str, optional): API key to include in headers.
        device_id (str, optional): Device ID to include in headers.
        token (str, optional): Bearer token for Authorization header.

    Returns:
        dict: Headers dictionary.
    """
    headers = {
        "accept": "*/*",                 # match cURL exactly
        "platform": platform,
        "language": "eng",               # match cURL exactly
        "TENANT_IDENTIFIER": "master",   # add missing header
        "local": "eng"
    }

    # Optional headers
    if x_api_key:
        headers["x-api-key"] = x_api_key
    if device_id:
        headers["device_id"] = device_id
    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers




ENDPOINTS = {
    "image_configs": "/config-service/pub/v1/image-configs",
    "operator_configs": "/config-service/pub/v1/operator-configs",
    "platform_configs": "/config-service/pub/v1/platform-configs",
    "menu_list": "/menu-service/pub/v1/menu"
}
