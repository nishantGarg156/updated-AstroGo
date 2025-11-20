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
        self.get_entitlements()
        self.tokenGenerationUWM()
        self.tokenGenerationCTG()

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
        log(resp.json())
        self.entitlementResponse = resp.json()

        check(resp, 200, "sessionId")


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

        self.uwmToken = resp.json().get("data", {}).get("cdnToken", {}).get("token")
        log(resp.json())
        log(self.movieContentId)
        log(self.uwmToken)

        check(resp, 200, "Watermark Token Generated successfully")



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

        self.ctgToken = resp.json().get("data", {}).get("drmToken", {}).get("token")
        log(resp.json())
        log(self.seriesContentId)
        log(self.ctgToken)

        check(resp, 200, "DRM Token Generated successfull")

