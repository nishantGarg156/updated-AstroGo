# utils/config.py

#BASE_URL = "https://api.vrgo.test.xp.irdeto.com"
import uuid


BASE_URL = "https://api.vrgo.load.xp.irdeto.com"

PLATFORM = "WEB"

 # generate random device_id


def get_headers(platform: str, x_api_key: str = None):
    headers = {
        "accept": "*/*",                # match cURL exactly
        "platform": platform,
        "language": "eng",              # match cURL exactly
        "TENANT_IDENTIFIER": "master",  # add missing header
        "local": "eng",
        "device_id": str(uuid.uuid4())                            # add missing header
    }
    if x_api_key:
        headers["x-api-key"] = x_api_key
    return headers


ENDPOINTS = {
    "image_configs": "/config-service/pub/v1/image-configs",
    "operator_configs": "/config-service/pub/v1/operator-configs",
    "platform_configs": "/config-service/pub/v1/platform-configs",
    "menu_list": "/menu-service/pub/v1/menu"
}
