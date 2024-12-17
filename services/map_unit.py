import json
import requests
from dotenv import load_dotenv
import os
import re

# Load the .env file
parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)  # Get the path of the parent directory
env_path = os.path.join(parent_dir, ".env")

load_dotenv(dotenv_path=env_path)

GOOGLE_MAP_API_KEY= os.getenv("GOOGLE_MAP_API_KEY")

# Simulating a configuration file to hold the API key
config = {
    "API_KEY": {
        "geocode": GOOGLE_MAP_API_KEY
    }
}


def get_geocode(location: str, api_key: str) -> dict:
    """
    Fetch the geocode (latitude and longitude) for a given location using the Google Maps Geocoding API.

    :param location: The name of the location to geocode.
    :param api_key: The API key for accessing Google Maps Geocoding API.
    :return: A dictionary containing latitude and longitude.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    url = f"{base_url}?address={location}&key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return {"lat": location["lat"], "lng": location["lng"]}
        else:
            raise Exception(f"Failed to get geocode: {data['status']}")
    else:
        raise Exception(f"Failed to fetch data from API: {response.status_code}")


def process_text(preference: str) -> int:
    """
    Convert user preference text into a numerical code.

    :param preference: User preference as a string ('省錢', '省時間', or '無').
    :return: A numerical code (0 for '省錢', 1 for '省時間' or '無').
    """
    # if preference == "省錢":
    #     return 0
    # elif preference in ["省時間", "無"]:
    #     return 1
    # else:
    #     raise Exception(f"Invalid input: {preference}")
    if preference == "省錢":
        return 0
    else:
        return 1


def get_result(input_string: str) -> str:
    """
    Process user input, fetch geocode data, and generate a result in JSON format.

    :param input_string: JSON string containing user input data.
    :return: A JSON string containing the result.
    """


    api_key = config["API_KEY"]["geocode"]

    try:
        # Parse the input JSON string
        # parsed_input = json.loads(json.loads(input_string)["data"])
        parsed_data = json.loads(input_string)["data"]

        cleaned_response = re.sub(r'```(json)?\n', '', parsed_data)  # Remove opening triple backticks
        cleaned_response = re.sub(r'\n```', '', cleaned_response)  # Remove closing triple backticks

        cleaned_response = cleaned_response.strip()

        parsed_input = json.loads(cleaned_response)

        origin_name = f"{parsed_input['origin']}(台灣)"
        destination_name = f"{parsed_input['destination']}(台灣)"
        preference = parsed_input["preference"]

        # Get geocode for origin and destination
        origin = get_geocode(origin_name, api_key)
        destination = get_geocode(destination_name, api_key)

        # Process user preference
        gc = process_text(preference)

        # Construct the result JSON object
        result = {
            "result": True,
            "data": {
                "origin": [origin["lng"], origin["lat"]],
                "destination": [destination["lng"], destination["lat"]],
                "gc": gc,
            },
        }

        return json.dumps(result)

    except Exception as e:
        # Handle errors and return a failure message
        return json.dumps({"result": False, "message": str(e)})


# Testing the function
if __name__ == "__main__":
    # Example input JSON string
    input_json = """
    {
        "data": {
            "origin": "板橋車站",
            "destination": "台北市政府",
            "preference": "省時間"
        }
    }
    """

    # Call the get_result function and print the output
    result = get_result(input_json)
    print(result)
