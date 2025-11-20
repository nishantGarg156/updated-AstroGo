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
        # # Now, self.access_token is available for all subsequent API calls
        # launch = LaunchJourney(self.client)
        # platform_data = launch.run()

        # self.platform_id = platform_data.get("platformId")
        # self.x_api_key = platform_data.get("xApiKey")
        # #Example: MenuListJourney
        # menu = MenuListJourney(self.client, self.platform_id, self.x_api_key)
        # tab_link = menu.run()
        # movie_tab_id = tab_link.get("Movies")
        # sports_tab_id = tab_link.get("Sports")

        token_gen = TokenGenerator(self.client, self.x_api_key, self.access_token)
        token_gen.run()

class FullUserFlow(HttpUser):
    wait_time = constant_throughput(0.05)  # ~1 journey every 20 sec per user
    tasks = [FullJourney]
    host = BASE_URL
