from locust import SequentialTaskSet, HttpUser, constant_throughput, task, LoadTestShape
from utils.config import BASE_URL
from scenarios.launch import LaunchJourney
from scenarios.login import LoginJourney
from scenarios.menuListUser import MenuListJourney
from scenarios.moviePage import MovieHierarchy
from scenarios.homePage import HomePageHierarchy
from scenarios.content import ContentDetail
from scenarios.sportsPage import SportPageHierarchy
import random

class FullJourney(SequentialTaskSet):

    @task
    def run_full_journey(self):
        # Step 1: Launch Journey
        launch = LaunchJourney(self.client)
        platform_data = launch.run()
        platform_id = platform_data.get("platformId")
        x_api_key = platform_data.get("xApiKey")

        menu = MenuListJourney(self.client, platform_id, x_api_key)
        tab_link = menu.run()
        movie_tab_id = tab_link.get("Movies")
        sports_tab_id = tab_link.get("Sports")

        home = HomePageHierarchy(self.client, x_api_key)
        home.run()

        if random.random() < 0.7 and sports_tab_id:
            sports = SportPageHierarchy(self.client, sports_tab_id, x_api_key)
            sports.run()

        if random.random() < 0.3 and movie_tab_id:
            movie = MovieHierarchy(self.client, movie_tab_id, x_api_key)
            movie.run()

        contentDetailPage = ContentDetail(self.client, x_api_key)
        contentDetailPage.run()

class FullUserFlow(HttpUser):
    wait_time = constant_throughput(0.05)  # ~1 journey every 20 sec per user
    tasks = [FullJourney]
    host = BASE_URL

class CustomLoadShape(LoadTestShape):
    """
    Ramp up to 1000 users in 30 sec (spawn_rate ~33.33/sec),
    hold for 5 min (300 sec), then ramp down to 0 in 30 sec.
    """
    stages = [
        {"duration": 60, "users": 1000, "spawn_rate": 17.33},   # ramp up
        {"duration": 300, "users": 1000, "spawn_rate": 0},      # hold
        {"duration": 60, "users": 0, "spawn_rate": 17.33},      # ramp down
    ]

    def tick(self):
        run_time = self.get_run_time()
        total_duration = 0
        for stage in self.stages:
            total_duration += stage["duration"]
            if run_time < total_duration:
                return (stage["users"], stage["spawn_rate"])
        return None