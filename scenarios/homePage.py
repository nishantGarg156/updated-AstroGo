from utils.assertion import check
from utils.config import BASE_URL, get_headers, PLATFORM

class HomePageHierarchy:
    def __init__(self, client, x_api_key):
        self.client = client
        self.x_api_key = x_api_key

    def run(self):
        headers = get_headers(PLATFORM, self.x_api_key)
        home_hierarchy_endpoint = "/homescreen-service/pub/v1/rail-hierarchy/5f45233ff0a4ca2277d30ca1?offset=0&limit=10"
        resp = self.client.get(BASE_URL + home_hierarchy_endpoint, headers=headers, name = "railHierarchy_homepage")
        check(resp, 200, "Rail fetched successfully")

        rail_ids = self.extract_rail_ids(resp)

        for rail_id in rail_ids[:5]:  # limit to 5 rail detail calls
            rail_detail_endpoint = f"/homescreen-service/pub/v1/rail/{rail_id}?offset=0&limit=20&entitlementFilteringEnabled=false"
            resp = self.client.get(BASE_URL + rail_detail_endpoint, headers=headers, name = "rail_id_homepage")
            check(resp, 200, "Content fetched successfully")

        

    def extract_rail_ids(self, response):
        json_data = response.json()
        results = json_data.get("data", {}).get("results", [])
        rail_ids = [item.get("id") for item in results if item.get("id")]
        return rail_ids



