# scenarios/content.py

import random
from time import time
from utils.assertion import check
from utils.config import BASE_URL, get_headers, PLATFORM, log
from utils.contentId_loader import ContentLoader

class ContentDetail:
    def __init__(self, client, x_api_key, deviceId):
        self.client = client
        self.x_api_key = x_api_key
        self.headers = get_headers(PLATFORM, self.x_api_key)
        self.deviceId = deviceId

        # Get random movie ID from content loader
        self.loader = ContentLoader()
        self.movie_id = self.loader.get_random_movie_id()
        self.channelIds = [
                        "9eeaf889-8810-43a1-aed9-fa249d140686",
                        "115daf54-e3a3-405d-a134-c5db006407c5",
                        "9bdedfe8-43d8-45d5-a2d3-426d3ad2785c",
                        "477a1cec-4200-4a49-8749-7cb3d2a80f2c",
                        "2fbb30a6-c065-4b7e-8e53-cdee7e3a4d53",
                        "0451f2ed-63a7-45bd-a8d0-2f2197d556b5"
                        ]
        
        self.series_ids = [
            "fdf02adc-9fe3-438f-8300-3e5a24d3c84a",
            "13f3b907-200c-4ec4-925a-d65ef8479a0b",
            "f896b39d-6a29-4ccd-8252-54e921fe171e",
            "aa7e9b5e-d742-41a9-bdef-d6dc934af109",
            "0514dab7-4044-4e92-bf83-ee607711e24a",
            "8bade1d5-b77e-47ae-b5c6-fa686f5118cc",
            "80f1f99a-69ff-4639-9d75-f11a46d8c62c",
            "398fba55-ca8f-4e8f-af21-f850ecd41bc7",
            "2076e890-a3e6-4ef1-832e-84181bf82543",
            "2076e890-a3e6-4ef1-832e-84181bf82543",
            "fdf02adc-9fe3-438f-8300-3e5a24d3c84a",
            "2283abb2-24a8-45de-a2b6-c106fcb3b403",
            "fdf02adc-9fe3-438f-8300-3e5a24d3c84a",
            "659747f3-3494-4ee0-afe9-0a331fe82ac5",
            "5ff1e3c8-6c41-4e86-8c0a-2e2e8d6ed702",
            "92eae78b-4fba-45d6-90d4-be12c2d1a97d",
            "ad89886d-a960-454b-a8c6-ff96dc538109",
            "d06ef9fd-341a-440c-8fed-f679affa888b",
            "ccf8b11d-82d6-4a2d-870b-d35db0aebf27",
            "927bcc81-99ab-4555-a8dd-58b8425f8a3a",
            "dae0965b-7967-47d9-9688-8458a107b633",
            "7e5003b4-7b5d-479b-80d6-884b7fd905d4",
            "188b1a35-486a-4e96-8379-5f5753099404",
            "26bbb1e7-84db-4974-827b-5c987f3a504e"
        ]
    def run(self):
        rand_val = random.random()

        if rand_val < 0.25:
            # 25% chance to call only MyBox API
            self.get_myBox()
            self.get_contentByFilter()
            self.get_miniMyBox()
            self.get_Channel_Dates()
            self.get_Channel_Day()
        else:
            # 75% chance to call both Movies and Series APIs
            if self.movie_id:
                self.get_movie_content()
                self.get_movie_trailer()
            else:
                log("[ERROR] No movie ID found in CSV.")

            if random.choice(self.series_ids):
                self.get_series_content()
                self.get_series_trailer()
                self.get_series_s1e1()
            else:
                log("[ERROR] No series ID found in CSV.")


    def get_movie_content(self):
        # Call movie detail API
        self.movie_id = self.loader.get_random_movie_id()
        movie_url = f"/content-detail-service/pub/v1/movie/{self.movie_id}"
        detail_resp = self.client.get(BASE_URL + movie_url, headers=self.headers, name="Movie Detail API")
        check(detail_resp, 200, "Content Fetched Successfully")

    def get_movie_trailer(self):
        # Call movie trailer API
        self.movie_id = self.loader.get_random_movie_id()
        trailer_url = f"/content-detail-service/pub/v1/trailer/movie/{self.movie_id}"
        trailer_resp = self.client.get(BASE_URL + trailer_url, headers=self.headers, name="Movie Trailer API")
        check(trailer_resp, 200, "Content Fetched Successfully")

    def get_series_content(self):
        self.series_id = self.loader.get_random_series_id()
        log(f"[INFO] Using series_id: {self.series_id}")
        series_url = f"/content-detail-service/pub/v1/series/{random.choice(self.series_ids)}"
        detail_resp = self.client.get(BASE_URL + series_url, headers=self.headers, name="Series API")
        check(detail_resp, 200, "Content Fetched Successfully")

        response_json = detail_resp.json()

        # Correct path to seasonList inside meta
        season_list = response_json.get("data", {}).get("meta", {}).get("seasonList", [])

        if not season_list:
            log(f"[WARN] No seasons found for series_id: {self.series_id}")
            log(f"[SKIPPING] Season API")
            return None

        first_season_id = season_list[0].get("id")
        log(f"First season id: {first_season_id}")

        self.first_season_id = first_season_id

        season_endpoint = f"/content-detail-service/pub/v1/season_episode/{first_season_id}?limit=1&offset=0&sort=asc"
        season_resp = self.client.get(BASE_URL + season_endpoint, headers=self.headers, name="Season API")
        check(season_resp, 200, "Content Fetched Successfully")

    def get_series_trailer(self):
        self.series_id = self.loader.get_random_series_id()
        log(f"[INFO] Using series_id: {self.series_id}")
        trailer_series_endpoint = f"/content-detail-service/pub/v1/trailer/series/{random.choice(self.series_ids)}"
        trailer_series_resp = self.client.get(BASE_URL + trailer_series_endpoint, headers=self.headers, name="Series Trailer API")
        check(trailer_series_resp, 200, "Content Fetched Successfully")

    def get_myBox(self):
        current_time_epoch_ms = int(time() * 1000)
        mybox_url = f"/content-detail-service/pub/v1/mybox/{current_time_epoch_ms}?offset=0&limit=100"
        mybox_resp = self.client.get(BASE_URL + mybox_url, headers=self.headers, name="MyBox API")
        check(mybox_resp, 200, "Content Fetched Successfully")

    def get_contentByFilter(self):
        filterApi_url = f"/content-detail-service/pub/v1/filter/"
        filterApi_resp = self.client.get(BASE_URL + filterApi_url, headers=self.headers, name="Filter API")
        check(filterApi_resp, 200, "Content Fetched Successfully")

    def get_miniMyBox(self):
        current_time_epoch_ms = int(time() * 1000)
        miniBox_url = f"/content-detail-service/pub/v1/mini-mybox/{current_time_epoch_ms}?offset=0&limit=50"
        miniBox_resp = self.client.get(BASE_URL + miniBox_url, headers=self.headers, name="MiniMyBox API")
        check(miniBox_resp, 200, "Content Fetched Successfully")

    def get_series_s1e1(self):

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.deviceId,
        )
    
        endpoint = f"/content-detail-service/pub/v1/s1e1/series/{random.choice(self.series_ids)}"

        headers.update({
            "cp_id": "60389013",
            "entitlementhash": "d6c37306b0447e8db311eec810033507c0168bc7",
            "environmentcode": "MAIN",
            "language": "eng",
            "languagecode": "eng",
            "local": "IND",
            "priority": "u=1, i",
            "profileid": self.deviceId,
            "profiletype": "ADULT"
        })


        url = BASE_URL + endpoint
        response = self.client.get(url, headers=headers, name="Series_s1e1 API")

        try:
            check(response, 200, "Content Fetched Successfully")
            response_json = response.json()
            log("[INFO] Series_S1E1 Content detail fetched successfully.", response_json)
            # log("Series ID Used: ", self.series_id, forcePrint=True)
            return response_json
        except Exception as e:
            log(f"[ERROR] Failed to fetch Series_S1E1 content detail: {e}")
            return None
    
    def get_Channel_Dates(self):

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.deviceId,
        )
        self.channelId = random.choice(self.channelIds)
    
        endpoint = f"/content-detail-service/pub/v1/channel/{self.channelId}/dates"

        headers.update({
            "cp_id": "60389013",
            "entitlementhash": "d6c37306b0447e8db311eec810033507c0168bc7",
            "environmentcode": "MAIN",
            "language": "eng",
            "languagecode": "eng",
            "local": "IND",
            "priority": "u=1, i",
            "profileid": self.deviceId,
            "profiletype": "ADULT"
        })


        url = BASE_URL + endpoint
        response = self.client.get(url, headers=headers, name="Channel_Dates API")

        try:
            check(response, 200, "Content Fetched Successfully")
            response_json = response.json()
            log("[INFO] Channel_Dates Content detail fetched successfully.", response_json)
            # log("Channel ID Used: ", self.channelId, forcePrint=True)
            return response_json
        except Exception as e:
            log(f"[ERROR] Failed to fetch Channel_Dates content detail: {e}")
            return None
    
    
    def get_Channel_Day(self):

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.deviceId,
        )
        self.channelId = random.choice(self.channelIds)
        current_time_epoch_ms = int(time() * 1000)
    
        endpoint = f"/content-detail-service/pub/v1/channel-day/{self.channelId}/{current_time_epoch_ms}"

        headers.update({
            "cp_id": "60389013",
            "entitlementhash": "d6c37306b0447e8db311eec810033507c0168bc7",
            "environmentcode": "MAIN",
            "language": "eng",
            "languagecode": "eng",
            "local": "IND",
            "priority": "u=1, i",
            "profileid": self.deviceId,
            "profiletype": "ADULT"
        })


        url = BASE_URL + endpoint
        response = self.client.get(url, headers=headers, name="Channel_Day API")

        try:
            check(response, 200, "Content Fetched Successfully")
            response_json = response.json()
            log("[INFO] Channel_Day Content detail fetched successfully.", response_json)
            # log("Channel ID Used: ", self.channelId, forcePrint=True)
            return response_json
        except Exception as e:
            log(f"[ERROR] Failed to fetch Channel_Day content detail: {e}")
            return None






