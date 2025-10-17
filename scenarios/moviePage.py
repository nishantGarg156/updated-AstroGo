from utils.assertion import check
from utils.config import BASE_URL, get_headers, PLATFORM

class MovieHierarchy:
    def __init__(self, client, movie_id, x_api_key):
        self.client = client
        self.movie_id = movie_id
        self.x_api_key = x_api_key

    def run(self):
        headers = get_headers(PLATFORM, self.x_api_key)

        hierarchy_endpoint = f"/homescreen-service/pub/v1/rail-hierarchy/{self.movie_id}?offset=0&limit=10"
        resp = self.client.get(BASE_URL + hierarchy_endpoint, headers=headers , name = "railHierarchy_MoviePage")

        check(resp, 200, "Rail fetched successfully")

        rail_ids = self.extract_rail_ids(resp)

        for rail_id in rail_ids[:4]:  # Limit to 4 rails if needed
            self.get_rail_details(rail_id, headers)

    def extract_rail_ids(self, response):
        json_data = response.json()
        results = json_data.get("data", {}).get("results", [])
        rail_ids = [item.get("id") for item in results if item.get("id")]
        return rail_ids

    def get_rail_details(self, rail_id, headers):
        rail_detail_endpoint = f"/homescreen-service/pub/v1/rail/{rail_id}?offset=0&limit=20&entitlementFilteringEnabled=false"
        resp = self.client.get(BASE_URL + rail_detail_endpoint, headers=headers, name = "railDetails_MoviePage")
        check(resp, 200, "Content fetched successfully")
