import requests
import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def download_file(file_url, token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    try:
        response = requests.get(file_url, headers=headers, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Extract the filename from the URL and prepend the /tmp directory
        filename = os.path.join('/tmp', file_url.split('/')[-1])
        
        # Write the content to a file /tmp
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"File successfully downloaded to {filename}")
        return filename  # Return the file path for further use if needed
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file: {e}")
        return None
    
def upload_file(client, user_token, channel_id, description, file_path):
    try:
        response = client.files_upload_v2(
            token=user_token,
            channel=channel_id,
            alt_txt="(AI-generated) "+description,
            file=file_path
        )
    except SlackApiError as e:
        assert e.response["error"] 
    
    
def delete_file(client, user_token, file_id):
    try:
        response = client.files_delete(
            token=user_token,
            file=file_id
            )
        print(f"File {file_id} deleted successfully")
    except SlackApiError as e:
        assert e.response["error"] 
