import requests
import json
from datetime import datetime, timedelta
from urllib.parse import urlencode
from dotenv import load_dotenv
import os

# Load the .env file
parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)  # Get the path of the parent directory
env_path = os.path.join(parent_dir, ".env")

load_dotenv(dotenv_path=env_path)

TDX_CLIENT_ID = os.getenv("TDX_CLIENT_ID")
TDX_CLIENT_SECRET = os.getenv("TDX_CLIENT_SECRET")


# Simulating a config.py configuration file
config = {"API_KEY": {"tdx": {"ID": TDX_CLIENT_ID, "Secret": TDX_CLIENT_SECRET}}}

auth_url = (
    "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
)


class TdxUnit:
    def __init__(self):
        self.access_token_info = {"access_token": "", "expire_time": datetime.now()}
        self.user_input = {
            "origin": [],
            "destination": [],
            "gc": 0,
            "transit": [3, 4, 5, 6, 7, 8, 9],
            "depart": datetime.now(),
            "arrival": datetime.now(),
        }

    @staticmethod
    def format_time(time: datetime) -> str:
        """Format datetime into the format required by the TDX API without over-encoding"""
        return time.strftime("%Y-%m-%dT%H:%M:%S")

    def update_user_input(self, input_data: dict):
        """Update user input"""
        self.user_input.update(
            {
                "origin": input_data["origin"],
                "destination": input_data["destination"],
                "gc": input_data["gc"],
                "transit": input_data["transit"],
                "depart": input_data["depart"],
                "arrival": input_data["arrival"],
            }
        )

    def get_url(self) -> str:
        """Generate the complete API URL"""
        transit_str = ",".join(map(str, self.user_input["transit"]))
        params = {
            "origin": f"{self.user_input['origin'][1]},{self.user_input['origin'][0]}",
            "destination": f"{self.user_input['destination'][1]},{self.user_input['destination'][0]}",
            "gc": self.user_input["gc"],
            "top": 1,
            "transit": transit_str,
            "transfer_time": "0,30",
            "depart": self.format_time(self.user_input["depart"]),
            "arrival": self.format_time(self.user_input["arrival"]),
            "first_mile_mode": 0,
            "first_mile_time": 30,
            "last_mile_mode": 0,
            "last_mile_time": 30,
        }
        base_url = "https://tdx.transportdata.tw/api/maas/routing"
        return f"{base_url}?{urlencode(params)}"

    def get_auth_header(self) -> dict:
        """Get authentication header"""
        return {"Content-Type": "application/x-www-form-urlencoded"}

    def get_auth_body(self) -> dict:
        """Get authentication request body"""
        return {
            "grant_type": "client_credentials",
            "client_id": config["API_KEY"]["tdx"]["ID"],
            "client_secret": config["API_KEY"]["tdx"]["Secret"],
        }

    def update_access_token(self):
        """Update the access token"""
        response = requests.post(
            auth_url, headers=self.get_auth_header(), data=self.get_auth_body()
        )
        response_data = response.json()
        self.access_token_info["access_token"] = response_data["access_token"]
        self.access_token_info["expire_time"] = datetime.now() + timedelta(
            seconds=response_data["expires_in"]
        )

    def get_access_token(self) -> str:
        """Retrieve a valid access token"""
        if (
            not self.access_token_info["access_token"]
            or datetime.now() >= self.access_token_info["expire_time"]
        ):
            self.update_access_token()
        return self.access_token_info["access_token"]

    def get_data_header(self, access_token: str) -> dict:
        """Get header for data request"""
        return {"Authorization": f"Bearer {access_token}", "Accept-Encoding": "gzip"}

    def get_result(self, input_string: str) -> str:
        """Process input and send a request to the API"""
        input_data = json.loads(input_string)

        if not input_data.get("result", False):
            return json.dumps(input_data)

        input_data["data"].update(
            {
                "transit": [3, 4, 5, 6, 7, 8, 9],
                "depart": datetime.now() + timedelta(minutes=5),
                "arrival": datetime.now() + timedelta(days=1),
            }
        )

        self.update_user_input(input_data["data"])

        access_token = self.get_access_token()
        response = requests.get(
            self.get_url(), headers=self.get_data_header(access_token)
        )
        response_data = response.json()

        if response_data.get("result") == "fail":
            return json.dumps(
                {
                    "result": False,
                    "message": response_data.get("error", "Unknown error"),
                }
            )
        elif not response_data.get("data", {}).get("routes", []):
            return json.dumps({"result": False, "message": "Route not found"})

        return json.dumps({"result": True, "data": response_data["data"]})


# For debugging and testing
if __name__ == "__main__":
    tdx_unit = TdxUnit()

    input_json = """
    {
        "result": true,
        "data": {
            "origin": [121.52017356684297, 25.06976766747735],
            "destination": [121.51976421101928, 25.06305755058022],
            "gc": 1
        }
    }
    """

    result = tdx_unit.get_result(input_json)
    print(f"Length of result: {len(result)}")
    print(f"Result: {result}")
