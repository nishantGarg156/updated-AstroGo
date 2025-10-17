from utils.config import BASE_URL

class LoginJourney:
    def __init__(self, client, user_data):
        self.client = client
        self.user_data = user_data
        self.token = None
        self.customer_id = None
        self.profile_id = None

    def run(self):
        username = self.user_data["username"]
        password = self.user_data["password"]

        print(f"[INFO] Logging in with → Username: {username}")

        login_endpoint = "/auth-service/pub/v1/login"
        login_payload = {
            "username": username,
            "password": password,
            "platform": "WEB",
            "rememberMe": True
        }

        response = self.client.post(BASE_URL + login_endpoint, json=login_payload)

        if response.status_code == 200:
            json_resp = response.json()

            # Assuming the token, customerId and profileId are inside the response JSON,
            # update these keys based on your actu
