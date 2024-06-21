import requests
import json

def generate_image_description(encoded_image, api_url):
    payload = {
        "model": "llava:34b",
        "stream": False,
        "prompt": "Please provide a detailed description of this image in 1000 characters or less.",
        "images": [encoded_image]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(f"{api_url}/api/generate", data=json.dumps(payload), headers=headers, verify=False)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    # Print the raw response content for debugging
    print(f"Raw response content: {response.content}")

    try:
        response_json = response.json()
        print(f"Response JSON: {response_json}")  # Debug print
        return response_json.get("response", "No response key in JSON")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}")
        return None
