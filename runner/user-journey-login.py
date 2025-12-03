
from locust import SequentialTaskSet, HttpUser, constant_throughput, task
from scenarios.tokenGenerator import TokenGenerator
from utils.config import BASE_URL
from scenarios.launch import LaunchJourney
from scenarios.login import LoginJourney
from scenarios.menuListUser import MenuListJourney
from scenarios.moviePage import MovieHierarchy
from scenarios.homePage import HomePageHierarchy
from scenarios.content import ContentDetail
from scenarios.sportsPage import SportPageHierarchy
from scenarios.continueWatch import ContinueWatch
from scenarios.fav import FavouritesJourney
from utils.assertion import check

import random


# -------------------------------
#     FULL JOURNEY TASK SET
# -------------------------------

class FullJourney(SequentialTaskSet):


    @task
    def run_full_journey(self):
        # Now, self.access_token is available for all subsequent API calls
        client = self.client
        x_api_key = self.user.x_api_key
        access_token = self.user.access_token
        platform_id = self.user.platform_id
        deviceId = self.user.deviceId
        #Example: MenuListJourney
        menu = MenuListJourney(client, platform_id, x_api_key)
        tab_link = menu.run()
        movie_tab_id = tab_link.get("Movies")
        sports_tab_id = tab_link.get("Sports")

        # Home Page APIs
        home = HomePageHierarchy(client, x_api_key)
        home.run()

        # ContinueWatch API
        cw = ContinueWatch(
            client,
            x_api_key=x_api_key,
            token=access_token,
            deviceId=deviceId
        )
        cw.run()

        fav = FavouritesJourney(
            client,
            x_api_key=x_api_key,
            token=access_token,
            deviceId=deviceId,
            content_type="MOVIE"
        )
        fav.run()
        # Sports page (optional)
        if random.random() < 0.7 and sports_tab_id:
            sports = SportPageHierarchy(client, sports_tab_id, x_api_key)
            sports.run()

        # Movie page (optional)
        if random.random() < 0.3 and movie_tab_id:
            movie = MovieHierarchy(client, movie_tab_id, x_api_key)
            movie.run()

        # Content details
        content_detail_page = ContentDetail(client, x_api_key, deviceId)
        content_detail_page.run()

        token_gen = TokenGenerator(client, x_api_key, access_token, deviceId)
        token_gen.run()


class FullUserFlow(HttpUser):
    """
    All users FIRST perform Launch + Login ONCE.
    Then repeatedly run FullJourney tasks based on constant_throughput.
    """
    wait_time = constant_throughput(0.017)  # ~1 journey every 20 sec per user
    tasks = [FullJourney]
    host = BASE_URL

    def on_start(self):
        # Step 1: Run LaunchJourney
        launch = LaunchJourney(self.client)
        platform_data = launch.run()

        self.platform_id = platform_data.get("platformId")
        self.x_api_key = platform_data.get("xApiKey")
        
        # Step 2: Login (one-time)
        login = LoginJourney(self.client, self.x_api_key)
        self.access_token, self.deviceId = login.run()
