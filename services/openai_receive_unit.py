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

OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

# Simulated config file for API key
config = {
    "API_KEY": {
        "openai": OPENAI_API_KEY  # Replace with your actual OpenAI API key
    }
}


def extract_info(question: str) -> str:
    """
    Sends a prompt to OpenAI API to extract origin, destination, and preference.

    :param question: The input sentence containing travel details.
    :return: The generated response content from OpenAI API.
    """
    # Define the system message for OpenAI
    system_message = {
        "role": "system",
        "content": "You are an assistant that extracts information and responds in JSON format."
    }

    # Define the user message with the structured prompt
    prompt = f"""
    從以下問句中提取起點、終點，以及偏好：省錢(最便宜)，或省時間(最快)，或是無偏好。
    若能順利提取起點、終點，就以下 json 格式回應：
    {{
      "origin": (中文地名),
      "destination": (中文地名),
      "preference":("省錢" or "省時間" or "無")
    }}
    如果找不到起點、或是找不到終點，就回應："error"

    問句：{question}
    """

    user_message = {
        "role": "user",
        "content": prompt
    }

    # Send the request to OpenAI ChatCompletion API
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model
            messages=[system_message, user_message],
            temperature=0.2,       # Controls creativity
            max_tokens=500,        # Limits the output length
            seed=6                 # Ensures reproducibility
        )

        # Extract the response content from the API output
        content = response.choices[0].message.content.strip()
        return content

    except Exception as e:
        # Return error details if the API call fails
        return f"Error: {str(e)}"


def is_valid_result(result: str) -> bool:
    """
    Validates the result to check if 'error' is present.

    :param result: The response content from OpenAI API.
    :return: True if the result is valid, otherwise False.
    """
    return "error" not in result


def get_result(input_string: str) -> str:
    """
    Main function to process input, call OpenAI API, and validate the result.

    :param input_string: The user-provided sentence in JSON format.
    :return: A JSON-formatted string containing success or failure message.
    """
    # Set the OpenAI API key
    openai.api_key = config['API_KEY']['openai']

    try:
        # Call the extract_info function to get the AI response
        result = extract_info(input_string)
        print("result: ", result)

        # Validate the result
        if not is_valid_result(result):
            return json.dumps({
                'result': False,
                'message': 'Origin or destination is not correct'
            }, ensure_ascii=False)

        # Return success response with extracted data
        return json.dumps({
            'result': True,
            'data': result
        }, ensure_ascii=False)

    except Exception as e:
        # Handle and return any errors that occur
        return json.dumps({
            'result': False,
            'message': str(e)
        }, ensure_ascii=False)


if __name__ == '__main__':
    # Example input string
    input_string = "我想從台灣大學去淡水漁人碼頭，請問最快的方式是什麼？"

    # Call the get_result function
    result = get_result(input_string)
    print(result)
