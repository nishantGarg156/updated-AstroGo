from utils.config import get_headers, BASE_URL, PLATFORM, log
from utils.assertion import check
from utils.contentId_loader import DeviceIdLoader
import json

class LoginJourney:
    def __init__(self, client, x_api_key, profile_type="adult"):
        self.client = client
        self.device_id = DeviceIdLoader.get_next_device_id()
        self.x_api_key = x_api_key
        self.profile_id = DeviceIdLoader.get_next_device_id()
        self.profile_type = profile_type
        self.token = None          # Token from code API
        self.subject_token = None  # Token from subject API

    def run(self):
        """Run the full login journey and return final subject token"""
        self.token = self.code_api()            # Step 1: Get token from code API
        self.subject_token = self.subject_api() # Step 2: Get token from subject API
        return self.subject_token               # Step 3: Return final token

    def code_api(self):
        """Call the code API and extract access token"""
        code_url = "/v1/auth/token"
        headers = get_headers(PLATFORM, x_api_key=self.x_api_key, device_id=self.device_id)
        headers.update({
            "accept": "application/json, text/plain, /",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://web.vrgo.load.xp.irdeto.com",
            "priority": "u=1, i",
            "referer": "https://web.vrgo.load.xp.irdeto.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        })

        data = {
            "code": "ory_ac_RVDyThvV9RFDqhAAP98QSwG1N1kArQ60CpVweeJyJhE.mt4jZ7UWIFF78xlvKH45_caHgOGpH72dluOIIq_crmQ",
            "grant_type": "urn:ietf:params:oauth:grant-type:authorization_code",
            "code_verifier": "W4QnOv2LpxKu4UCtMt59o4Y5YO12rJUS4nvw6cHeJDWAET-JjwwGHfcU0nIw32",
            "device_details": json.dumps({
                "deviceFamilyId": "crm",
                "appVersion": "web-test-go-v5.0.35",
                "maxResolution": 1117,
                "audioCodecEac3": False,
                "audioCodecAc3": False,
                "videoCodecHevc": False,
                "friendlyName": "Chrome 141.0.7390.55",
                "osName": "Mac OS",
                "osVersion": "Mac OS",
                "browserName": "Chrome",
                "browserVersion": "141.0.7390.55"
            }),
            "redirect_uri": "https://web.vrgo.load.xp.irdeto.com",
            "device_id": self.device_id
        }

        resp = self.client.post(BASE_URL + code_url, headers=headers, data=data)
        # log(f"[INFO] Code API response status: {resp.status_code} for device_id: {self.device_id}")
        # log(f"[INFO] Code API response body: {resp.text}")
        check(resp, 200)

        try:
            resp_json = resp.json()
            access_token = resp_json.get("access_token")
            if not access_token:
                raise Exception("access_token not found in code API response")
            return access_token
        except json.JSONDecodeError:
            raise Exception("Failed to parse JSON response from code API")

    def subject_api(self):
        """Call the subject token API using token from code API"""
        subject_url = "/v1/auth/token"  # Replace with correct endpoint if different
        headers = get_headers(PLATFORM, x_api_key=self.x_api_key, device_id=self.device_id, token=self.token )  
        headers.update({
            "accept": "application/json",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://web.vrgo.load.xp.irdeto.com",
            "priority": "u=1, i",
            "referer": "https://web.vrgo.load.xp.irdeto.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        })

        data = {
            "subject_token": self.token,
            "subject_token_type": "Bearer",
            "profile_id": self.profile_id,
            "profile_type": self.profile_type
        }

        resp = self.client.post(BASE_URL + subject_url, headers=headers, data=data , name = "Subject_API_Login")
        # log(f"[INFO] Subject API response status: {resp.status_code}")
        # log(f"[INFO] Subject API response body: {resp.text}")
        check(resp, 200, "configurationKey")

        try:
            resp_json = resp.json()
            access_token = resp_json.get("access_token")
            if not access_token:
                raise Exception("access_token not found in subject API response")
            return access_token
        except json.JSONDecodeError:
            raise Exception("Failed to parse JSON response from subject API")