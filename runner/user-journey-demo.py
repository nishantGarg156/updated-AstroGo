from locust import SequentialTaskSet, HttpUser, constant_throughput, task
from utils.config import BASE_URL
from scenarios.launch import LaunchJourney
from scenarios.login import LoginJourney
from scenarios.menuListUser import MenuListJourney
from scenarios.moviePage import MovieHierarchy
from scenarios.homePage import HomePageHierarchy
from scenarios.content import ContentDetail
from scenarios.sportsPage import SportPageHierarchy
from utils.assertion import check
from utils.contentId_loader import UserCredentialLoader
import random

class FullJourney(SequentialTaskSet):

    def on_start(self):
        # Load unique user credentials once per virtual user, login only once here
        self.user_data = UserCredentialLoader.get_next_credential()
        if not self.user_data:
            raise Exception("No more user credentials available.")

        # Run login once per virtual user
        login = LoginJourney(self.client, self.user_data)
        login_resp = login.run()

        # Save token and other data for reuse
        self.token = login.token
        self.customer_id = login.customer_id
        self.profile_id = login.profile_id

        # Update client headers with token for all future requests
        if self.token:
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})

    @task
    def run_full_journey(self):
        print(f"[INFO] Starting full journey for user: {self.user_data['username']}")

        # Run LaunchJourney on every task iteration (so it's called repeatedly)
        launch = LaunchJourney(self.client)
        platform_data = launch.run()
        platform_id = platform_data.get("platformId")
        x_api_key = platform_data.get("xApiKey")

        # Now you can use platform_id, x_api_key, and self.token for other journeys

        # For example: MenuListJourney, HomePageHierarchy etc.

        # menu = MenuListJourney(self.client, platform_id, x_api_key)
        # tab_link = menu.run()
        # movie_tab_id = tab_link.get("Movies")
        # sports_tab_id = tab_link.get("Sports")

        # home = HomePageHierarchy(self.client, x_api_key)
        # home.run()

        # if random.random() < 0.7 and sports_tab_id:
        #     sports = SportPageHierarchy(self.client, sports_tab_id, x_api_key)
        #     sports.run()

        # if random.random() < 0.3 and movie_tab_id:
        #     movie = MovieHierarchy(self.client, movie_tab_id, x_api_key)
        #     movie.run()

        # content_detail_page = ContentDetail(self.client, x_api_key)
        # content_detail_page.run()


class FullUserFlow(HttpUser):
    wait_time = constant_throughput(0.05)  # ~1 journey every 20 sec per user
    tasks = [FullJourney]
    host = BASE_URL
