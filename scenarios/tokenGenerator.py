import json
from utils.assertion import check
from utils.config import BASE_URL, get_headers, PLATFORM, log
from utils.contentId_loader import DeviceIdLoader, ContentLoader

class TokenGenerator:
    def __init__(self, client, x_api_key, token):
        self.client = client
        self.token = token
        self.x_api_key = x_api_key
        self.deviceId = DeviceIdLoader.get_next_device_id()
        # self.movieContentId = ContentLoader().get_random_movie_id()
        # self.seriesContentId = ContentLoader().get_random_series_id()

    def run(self):
        self.movieContentId = ContentLoader().get_random_movie_id()
        self.seriesContentId = ContentLoader().get_random_series_id()
        self.entitlementResponse = self.get_entitlements()
        self.uwmToken = self.tokenGenerationUWM()
        self.ctgToken = self.tokenGenerationCTG()

# ---------------------------------------------------
# GET Entitlements
# ---------------------------------------------------
    def get_entitlements(self):
        endpoint = "/v1/entitlements"

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.deviceId,
            token=self.token
        )

        resp = self.client.get(
            BASE_URL + endpoint,
            headers=headers,
            name="entitlments_API"
        )


        try:
            check(resp, 200, "sessionId")
            resp_json = resp.json()
            log(resp_json)
            return resp_json
        except json.JSONDecodeError:
            log("[ERROR] Failed to parse JSON response from Entitlements API")


# ---------------------------------------------------
# POST token Generation UWM
# ---------------------------------------------------
    def tokenGenerationUWM(self):
        endpoint = "/token-generator-service/v2/uwm?isStatic=false&previewTokenRequired=true"

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.deviceId,
            token=self.token
        )

        headers.update({
            "Content-Type": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "local": "IND"
        })

        payload = {
            "type": 0,
            "isWMAuthEnabled": None,
            "isCDNAuthEnabled": None,
            "contentType": "movie",
            "contentId": f"{self.movieContentId}",
            "sessionInfo": self.entitlementResponse
        }

        resp = self.client.post(
            BASE_URL + endpoint,
            headers=headers,
            json=payload,
            name="tokenGenerationUWM"
        )

        try:
            check(resp, 200, "Watermark Token Generated successfully")
            resp_json = resp.json()
            cdnToken = resp_json.get("data", {}).get("cdnToken", {}).get("token")
            log(" CDN TOKEN >>>>", cdnToken)
            if not cdnToken:
                log(f"[ERROR] UWM Token not found in response: {resp_json}")
                log(f"[ERROR] Movie Content used: {self.movieContentId}")
            return cdnToken
        except json.JSONDecodeError:
            log("[ERROR] Failed to parse JSON response from UWM token generation")



# ---------------------------------------------------
# POST token Generation CTG
# ---------------------------------------------------
    def tokenGenerationCTG(self):
        endpoint = "/token-generator-service/v1/ctg?isStatic=false"

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.deviceId,
            token=self.token
        )

        headers.update({
            "Content-Type": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "local": "IND"
        })

        payload = {
            "type": 0,
            "isWMAuthEnabled": None,
            "isCDNAuthEnabled": None,
            "contentType": "series",
            "contentId": f"{self.seriesContentId}",
            "sessionInfo": self.entitlementResponse
        }

        resp = self.client.post(
            BASE_URL + endpoint,
            headers=headers,
            json=payload,
            name="tokenGenerationCTG"
        )

        try:
            check(resp, 200, "DRM Token Generated successfull")
            resp_json = resp.json()
            drmToken = resp_json.get("data", {}).get("drmToken", {}).get("token")
            log(" DRM TOKEN >>>>", drmToken)
            if not drmToken:
                log(f"[ERROR] CTG Token not found in response: {resp_json}")
                log(f"[ERROR] Series Content used: {self.seriesContentId}")
            return drmToken
        except json.JSONDecodeError:
            log("[ERROR] Failed to parse JSON response from CTG token generation")

