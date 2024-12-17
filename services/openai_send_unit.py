import openai
import json
from dotenv import load_dotenv
import os

# Load the .env file
parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)  # Get the path of the parent directory
env_path = os.path.join(parent_dir, ".env")

load_dotenv(dotenv_path=env_path)

OPANAI_API_KEY= os.getenv("OPANAI_API_KEY")

# Simulated config file for API key
config = {
    "API_KEY": {
        "openai": OPANAI_API_KEY  # Replace this with your OpenAI API key
    }
}

def extract_info(question: str) -> str:
    """
    Sends a prompt to the OpenAI API and retrieves the generated content.

    :param question: The input JSON text containing travel data.
    :return: The generated response text.
    """
    # Define the system message to set up the assistant's role
    system_message = {
        "role": "system",
        "content": "You are a geography assistant, who is good at organising. "
                   "Your job is to compose an instruction article."
    }

    # Define the user message with detailed instructions
    prompt = f"""
Read the information below, then write an instruction article in traditional Chinese colloquially.
Notice:
- You are an enthusiastic tour guide. You are talking to only one person.
- Time is represented by second now. Convert all the time representations into minute, hour, or day.
- Format date as "month/day hour:minute". Don't show year. E.g. 06/20 23:04.
- Don't show longitude nor latitude.
- For each traveling section, organize a paragraph.
- Label the sections with numbers.
- Don't use markdown syntax.
- MRT is 捷運.
- Start the article with greeting, fare, overall traveling time, departing and arrival time. Continue with 交通資訊.

json text:
{question}
"""
    user_message = {
        "role": "user",
        "content": prompt
    }

    # Combine system and user messages
    messages = [system_message, user_message]

    try:
        # Send a request to OpenAI Chat API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=1024,
            seed=6
        )

        # Extract the response content
        # response_content = response['choices'][0]['message']['content'].strip()
        response_content = response.choices[0].message.content.strip()
        return response_content

    except Exception as e:
        # Return an error message if the request fails
        return f"Error: {str(e)}"


def get_result(input_string: str) -> str:
    """
    Processes the input, calls extract_info, and returns a JSON result.

    :param input_string: The input JSON string with travel information.
    :return: A JSON-formatted result containing the response or an error message.
    """
    # Set the OpenAI API key
    openai.api_key = config['API_KEY']['openai']

    try:
        # Call the extract_info function to get the response from OpenAI
        result = extract_info(input_string)

        # Wrap the response in a JSON result
        return json.dumps({'result': True, 'data': result}, ensure_ascii=False)

    except Exception as e:
        # Handle errors and return a JSON error response
        return json.dumps({'result': False, 'message': str(e)}, ensure_ascii=False)


if __name__ == '__main__':
    # Example input JSON string
    input_string = '''
    {
        "result": "success",
        "data.routes": [
            {
                "travel_time": 481,
                "start_time": "2024-06-17T06:55:45",
                "day": 1,
                "end_time": "2024-06-17T07:03:46",
                "transfers": 0,
                "sections": [
                    {
                        "type": "pedestrian",
                        "actions": [
                            {"action": "depart", "duration": 103},
                            {"action": "arrive", "duration": 0}
                        ],
                        "travelSummary": {"duration": 103, "length": 144.16507},
                        "departure": {"time": "2024-06-17T06:55:45"},
                        "arrival": {"time": "2024-06-17T06:57:28", "place": {"name": "圓山站 出口1"}}
                    },
                    {
                        "type": "transit",
                        "travelSummary": {"duration": 88},
                        "departure": {"time": "2024-06-17T06:58:56", "place": {"name": "圓山"}},
                        "arrival": {"time": "2024-06-17T07:00:24", "place": {"name": "民權西路"}},
                        "transport": {"mode": "MRT", "name": "淡水信義線"}
                    }
                ]
            }
        ]
    }
    '''

    # Call the get_result function with the example input
    result = get_result(input_string)
    print(result[:500])  # Print the first 500 characters of the result
