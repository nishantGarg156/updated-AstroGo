import json
import random
from utils.config import get_headers, BASE_URL, PLATFORM, log
from utils.contentId_loader import DeviceIdLoader, ContentLoader
from utils.assertion import check


class ContinueWatch:
    def __init__(self, client, x_api_key, token):
        self.client = client
        self.x_api_key = x_api_key
        self.token = token

        # Load movie ID
        loader = ContentLoader()
        self.movie_id = loader.get_random_movie_id()

        # Device + Profile IDs from CSV
        self.device_id = DeviceIdLoader.get_next_device_id()
        self.profile_id = DeviceIdLoader.get_next_device_id()

        # Hardcoded subscriberId as per curl
        self.subscriber_id = "60388994"

    def run(self):
        """Run both GET and POST continue-watch APIs"""
        self.get_continue_watch()
        self.post_continue_watch()
        self.get_recent_continue_watch()

    # ---------------------------------------------------
    # GET Continue Watch List
    # ---------------------------------------------------
    def get_continue_watch(self):
        endpoint = "/subscriber-event-service/v3/continue-watch/continue?region=Malaysia&offset=0&limit=11"

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.device_id,
            token=self.token
        )

        headers.update({
            "accept": "application/json",
            "profileId": self.profile_id,
        })

        resp = self.client.get(
            BASE_URL + endpoint,
            headers=headers,
            name="Get_ContinueWatch"
        )

        check(resp, 200, "Data Fetched Successfully")


    # ---------------------------------------------------
    # POST Subscriber Continue Watch
    # ---------------------------------------------------
    def post_continue_watch(self):
        endpoint = "/subscriber-activity-producer/v3/subscriber-continue-watch"

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.device_id,
            token=self.token
        )

        # Copy curl-style headers
        headers.update({
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "cp_id": self.subscriber_id,
            "entitlementhash": "6394cc961095166f34011486129510521be23aa7",
            "environmentcode": "MAIN",
            "languagecode": "eng",
            "local": "IND",
            "origin": "https://web.vrgo.load.xp.irdeto.com",
            "priority": "u=1, i",
            "profileid": self.profile_id,
            "profiletype": "ADULT",
            "requestcount": "1",
            "tenant_identifier": "master"
        })

        # Random watch duration between 120–400 seconds
        watch_duration = random.randint(120, 400)

        payload = {
            "contentId": self.movie_id,
            "contentType": "VOD",
            "watchDuration": watch_duration,
            "subscriberId": self.subscriber_id
        }

        resp = self.client.post(
            BASE_URL + endpoint,
            headers=headers,
            json=payload,
            name="Add_To_ContinueWatch"
        )

        log("POST Continue Watch Response >>>", resp.text)

        check(resp, 200 , "Success")


    def get_recent_continue_watch(self):
        endpoint = (
            f"/subscriber-event-service/v3/continue-watch/content/recent"
            f"?contentType=VOD&region=Malaysia&contentId={self.movie_id}"
        )

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.device_id,
            token=self.token
        )

        # Copy curl-style headers
        headers.update({
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cp_id": self.subscriber_id,
            "entitlementhash": "6394cc961095166f34011486129510521be23aa7",
            "environmentcode": "MAIN",
            "language": "eng",
            "languagecode": "eng",
            "local": "IND",
            "origin": "https://web.vrgo.load.xp.irdeto.com",
            "platform": "WEB",
            "priority": "u=1, i",
            "profileid": self.profile_id,
            "profiletype": "ADULT",
            "requestcount": "1",
            "tenant_identifier": "master"
        })

        resp = self.client.get(BASE_URL + endpoint, headers=headers, name="Recent")

        log("GET Recent Continue Watch Response >>>", resp.text)

        check(resp, 200)
