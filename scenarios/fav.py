from utils.config import get_headers, BASE_URL, PLATFORM
from utils.assertion import check
from utils.contentId_loader import DeviceIdLoader, ContentLoader
import json
import random
import time


class FavouritesJourney:
    def __init__(self, client, x_api_key, token, content_type="MOVIE"):
        self.client = client
        self.x_api_key = x_api_key
        self.token = token
        self.content_type = content_type  

        # Load random movie/content ID
        loader = ContentLoader()
        self.movie_id = loader.get_random_movie_id()

        # Device + Profile ID
        self.device_id = DeviceIdLoader.get_next_device_id()
        self.profile_id = DeviceIdLoader.get_next_device_id()

        # Random CP_ID (8 digits)
        self.cp_id = str(random.randint(10000000, 99999999))

    def run(self):
        """Main entry for Locust"""
        
        # 10% chance to add to favourites
        if random.random() < 0.1:
            self.add_to_favourites_movie()
            time.sleep(1)  # wait 1 sec before next action

        # Always get favourites list (100% chance)
        self.get_favourites_list()

        # 10% chance to remove from favourites
        if random.random() < 0.1:
            time.sleep(1)  # optional delay before remove
            self.remove_favourite_movie()
        

    def add_to_favourites_movie(self):
        """POST favourite API"""
        endpoint = "/subscriber-event-service/v3/favourites"

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.device_id,
            token=self.token
        )

        headers.update({
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,hi;q=0.8",
            "content-type": "application/json",
            "cp_id": self.cp_id,
            "entitlementhash": "testHash001",
            "environmentcode": "MAIN",
            "language": "eng",
            "languagecode": "eng",
            "local": "IND",
            "platform": "WEB",
            "profileid": self.profile_id,
            "profiletype": "KIDS",
        })

        payload = {
            "contentId": self.movie_id,
            "contentType": self.content_type 
        }

        resp = self.client.post(BASE_URL + endpoint,headers=headers,json=payload,name="Add_to_Favourite")

        check(resp, 200, "Favourite")



    def get_favourites_list(self):
        """GET favourite list API"""
        endpoint = "/subscriber-event-service/v3/favourites?offset=0&limit=20&contentTypes=VOD"

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.device_id,
            token=self.token
        )

        # Add additional headers exactly like CURL
        headers.update({
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,hi;q=0.8",
            "cp_id": self.cp_id,
            "environmentcode": "MAIN",
            "language": "eng",
            "languagecode": "eng",
            "local": "IND",
            "platform": "WEB",
            "profileid": self.profile_id,
            "origin": "https://web.vrgo.load.xp.irdeto.com",
            "referer": "https://web.vrgo.load.xp.irdeto.com/",
            "requestcount": "1",
            "tenant_identifier": "master",
            "priority": "u=1, i"
        })

        resp = self.client.get(
            BASE_URL + endpoint,
            headers=headers,
            name="Get_Favourite_List"
        )

        #print("GET Favourite List Response >>>>>>>", resp.text)
        check(resp, 200)


    def remove_favourite_movie(self):
        """DELETE favourite by contentId"""

        # DELETE endpoint needs contentId appended
        endpoint = f"/subscriber-event-service/v3/favourites/{self.movie_id}"

        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.device_id,
            token=self.token
        )

        # Matching headers from curl
        headers.update({
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "cp_id": self.cp_id,
            "entitlementhash": "6394cc961095166f34011486129510521be23aa7",
            "environmentcode": "MAIN",
            "language": "eng",
            "languagecode": "eng",
            "local": "IND",
            "origin": "https://web.vrgo.test.xp.irdeto.com",
            "platform": "WEB",
            "priority": "u=1, i",
            "profileid": self.profile_id,
            "profiletype": "ADULT",
            "requestcount": "1",
            "tenant_identifier": "master",
        })

        resp = self.client.delete(
            BASE_URL + endpoint,
            headers=headers,
            json={},     # DELETE still has a body in curl
            name="Remove_Favourite"
        )

       # print("Remove Favourite Response >>>>>>>>>", resp.text)

        check(resp, 200)

    def get_purchased_rail(self):
        endpoint = (
            "/homescreen-service/pub/v1/purchased-rail"
            "?limit=20&offset=0&contentType=VOD,BOXSET&isEntitlementEnabled=true"
        )

        # Base headers
        headers = get_headers(
            PLATFORM,
            x_api_key=self.x_api_key,
            device_id=self.device_id,
            token=self.token
        )

        # Additional curl headers
        headers.update({
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "cp_id": self.cp_id,
            "entitlementhash": "6394cc961095166f34011486129510521be23aa7",
            "environmentcode": "MAIN",
            "isentitlementenabled": "true",
            "language": "eng",
            "languagecode": "eng",
            "local": "IND",
            "origin": "https://web.vrgo.test.xp.irdeto.com",
            "platform": "WEB",
            "priority": "u=1, i",
            "profileid": self.profile_id,
            "profiletype": "ADULT",
            "referer": "https://web.vrgo.test.xp.irdeto.com/",
            "requestcount": "1",
            "tenant_identifier": "master",
        })

        resp = self.client.get(
            BASE_URL + endpoint,
            headers=headers,
            name="Purchased_Rail"
        )

        print("GET Purchased Rail Response >>>", resp.text)

        check(resp, 200, "purchased")



