# scenarios/content.py

import random
from time import time
from utils.assertion import check
from utils.config import BASE_URL, get_headers, PLATFORM, log
from utils.contentId_loader import ContentLoader

class ContentDetail:
    def __init__(self, client, x_api_key):
        self.client = client
        self.x_api_key = x_api_key
        self.headers = get_headers(PLATFORM, self.x_api_key)

        # Get random movie ID from content loader
        loader = ContentLoader()
        self.movie_id = loader.get_random_movie_id()
        self.series_id = loader.get_random_series_id()
        log(f"[INFO] Using series_id: {self.series_id}")

    def run(self):
        rand_val = random.random()

        if rand_val < 0.25:
            # 25% chance to call only MyBox API
            self.get_myBox()
        else:
            # 75% chance to call both Movies and Series APIs
            if self.movie_id:
                self.get_movie_content()
            else:
                log("[ERROR] No movie ID found in CSV.")

            if self.series_id:
                self.get_series_content()
            else:
                log("[ERROR] No series ID found in CSV.")


    def get_movie_content(self):
        # Call movie detail API
        movie_url = f"/content-detail-service/pub/v1/movie/{self.movie_id}"
        detail_resp = self.client.get(BASE_URL + movie_url, headers=self.headers, name="Movie Detail API")
        check(detail_resp, 200, "Content Fetched Successfully")

        # Call movie trailer API
        trailer_url = f"/content-detail-service/pub/v1/trailer/movie/{self.movie_id}"
        trailer_resp = self.client.get(BASE_URL + trailer_url, headers=self.headers, name="Movie Trailer API")
        check(trailer_resp, 200, "Content Fetched Successfully")

    def get_series_content(self):
     series_url = f"/content-detail-service/pub/v1/series/{self.series_id}"
     detail_resp = self.client.get(BASE_URL + series_url, headers=self.headers, name="Series API")
     check(detail_resp, 200, "Content Fetched Successfully")

     response_json = detail_resp.json()

     # Correct path to seasonList inside meta
     season_list = response_json.get("data", {}).get("meta", {}).get("seasonList", [])

     if not season_list:
        log(f"[WARN] No seasons found for series_id: {self.series_id}")
        return None

     first_season_id = season_list[0].get("id")
     log(f"First season id: {first_season_id}")

     self.first_season_id = first_season_id

     season_endpoint = f"/content-detail-service/pub/v1/season_episode/{first_season_id}?limit=1&offset=0&sort=asc"
     season_resp = self.client.get(BASE_URL + season_endpoint, headers=self.headers, name="Season API")
     check(season_resp, 200, "Content Fetched Successfully")

     trailer_series_endpoint = f"/content-detail-service/pub/v1/trailer/series/{self.series_id}"
     trailer_series_resp = self.client.get(BASE_URL + trailer_series_endpoint, headers=self.headers, name="Series Trailer API")
     check(trailer_series_resp, 200, "Content Fetched Successfully")

    def get_myBox(self):
        ccurrent_time_epoch_ms = int(time() * 1000)
        mybox_url = f"/content-detail-service/pub/v1/mybox/{ccurrent_time_epoch_ms}?offset=0&limit=100"
        mybox_resp = self.client.get(BASE_URL + mybox_url, headers=self.headers, name="MyBox API")
        check(mybox_resp, 200, "Content Fetched Successfully")

        filterApi_url = f"/content-detail-service/pub/v1/filter/"
        filterApi_resp = self.client.get(BASE_URL + filterApi_url, headers=self.headers, name="Filter API")
        check(filterApi_resp, 200, "Content Fetched Successfully")

        miniBox_url = f"/content-detail-service/pub/v1/mini-mybox/{ccurrent_time_epoch_ms}?offset=0&limit=50"
        miniBox_resp = self.client.get(BASE_URL + miniBox_url, headers=self.headers, name="MiniMyBox API")
        check(miniBox_resp, 200, "Content Fetched Successfully")
    
     




