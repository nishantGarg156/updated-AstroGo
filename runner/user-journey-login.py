
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

class FullJourney(SequentialTaskSet):

    def on_start(self):
        # Step 1: Run LaunchJourney
        launch = LaunchJourney(self.client)
        platform_data = launch.run()

        self.platform_id = platform_data.get("platformId")
        self.x_api_key = platform_data.get("xApiKey")
        
        # Step 2: Run LoginJourney and get subject token
        login = LoginJourney(self.client, self.x_api_key)
        self.access_token = login.run()  # This is subject token from subject_api

    @task
    def run_full_journey(self):
        # Now, self.access_token is available for all subsequent API calls
        launch = LaunchJourney(self.client)
        platform_data = launch.run()

        # self.platform_id = platform_data.get("platformId")
        # self.x_api_key = platform_data.get("xApiKey")
        #Example: MenuListJourney
        menu = MenuListJourney(self.client, self.platform_id, self.x_api_key)
        tab_link = menu.run()
        movie_tab_id = tab_link.get("Movies")
        sports_tab_id = tab_link.get("Sports")

        # Home Page APIs
        home = HomePageHierarchy(self.client, self.x_api_key)
        home.run()

        # ContinueWatch API
        cw = ContinueWatch(
            self.client,
            x_api_key=self.x_api_key,
            token=self.access_token,
        )
        cw.run()

        fav = FavouritesJourney(
            self.client,
            x_api_key=self.x_api_key,
            token=self.access_token,
            content_type="MOVIE"
        )
        fav.run()
        # Sports page (optional)
        if random.random() < 0.7 and sports_tab_id:
            sports = SportPageHierarchy(self.client, sports_tab_id, self.x_api_key)
            sports.run()

        # Movie page (optional)
        if random.random() < 0.3 and movie_tab_id:
            movie = MovieHierarchy(self.client, movie_tab_id, self.x_api_key)
            movie.run()

        # Content details
        content_detail_page = ContentDetail(self.client, self.x_api_key)
        content_detail_page.run()

        token_gen = TokenGenerator(self.client, self.x_api_key, self.access_token)
        token_gen.run()


class FullUserFlow(HttpUser):
    wait_time = constant_throughput(0.017)  # ~1 journey every 20 sec per user
    tasks = [FullJourney]
    host = BASE_URL
