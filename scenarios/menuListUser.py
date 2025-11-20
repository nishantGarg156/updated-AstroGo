from utils.config import BASE_URL
from utils.assertion import check

class MenuListJourney:
    def __init__(self, client, platform_id, x_api_key):
        self.client = client
        self.platform_id = platform_id
        self.x_api_key = x_api_key

    def run(self):
        headers = {
            "accept": "application/json",
            "languageCode": "eng",
            "x-api-key": self.x_api_key
        }

        endpoint = f"/homescreen-service/pub/v2/menu/list/platformId?platformId={self.platform_id}"
        resp = self.client.get(BASE_URL + endpoint, headers=headers)
        check(resp, 200, "Data fetched Successfully")

        json_data = resp.json()
        menu_list = json_data.get("data", {}).get("menuDataList", [])

        # Target tab names to extract (lowercase for matching)
        target_tabs = ["movies", "tv shows", "sports"]

        # Final dictionary to store {tabName: linkToPage}
        tab_link_map = {}

        for item in menu_list:
            tab_name = item.get("tabName", "")
            tab_name_lower = tab_name.lower()

            if tab_name_lower in target_tabs:
                tab_link_map[tab_name] = item.get("linkToPage")  # Preserve original casing

        # print("\n✅ Extracted tabName → linkToPage:")
        # for tab, link in tab_link_map.items():
        #     print(f"  {tab}: {link}")

        return tab_link_map
