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
    wait_time = constant_throughput(0.017)  # ~1 journey every 20 sec per user
    tasks = [FullJourney]
    host = BASE_URL
