from utils.config import BASE_URL, ENDPOINTS, get_headers, PLATFORM
from utils.assertion import check

class LaunchJourney:
    def __init__(self, client):
        self.client = client

    def run(self):
        self.get_image_configs()
        self.get_operator_configs()
        platform_data = self.get_platform_configs()
        return platform_data  # contains platformId and xApiKey

    def get_image_configs(self):
        resp = self.client.get(BASE_URL + ENDPOINTS["image_configs"], headers=get_headers(PLATFORM))
        check(resp, 200, "image config fetched successfully")

    def get_operator_configs(self):
        resp = self.client.get(BASE_URL + ENDPOINTS["operator_configs"], headers=get_headers(PLATFORM))
        check(resp, 200, "operator fetched successfully")

    def get_platform_configs(self):
        resp = self.client.get(BASE_URL + ENDPOINTS["platform_configs"], headers=get_headers(PLATFORM))
        check(resp, 200, "WEB platform fetched successfully")

        data = resp.json()["data"][0]["data"]
        return {
            "platformId": data.get("platformId"),
            "xApiKey": data.get("cdnAuthKey")
        }