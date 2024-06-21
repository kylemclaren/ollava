import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
from handlers import command_handlers
import base64
import json
from utils.file_helpers import download_file, delete_file, upload_file
from utils.api_helpers import generate_image_description

# Set up logging
logging.basicConfig(level=logging.os.environ.get('LOG_LEVEL', 'DEBUG'))

oauth_settings = OAuthSettings(
    client_id=os.environ["SLACK_CLIENT_ID"],
    client_secret=os.environ["SLACK_CLIENT_SECRET"],
    scopes=["channels:read", "files:read", "files:write"],
    user_scopes=["channels:read", "files:read", "files:write"],
    user_token_resolution="actor",
    installation_store=FileInstallationStore(base_dir="./data/installations"),
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="./data/states")
)

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    oauth_settings=oauth_settings
)

def get_user_token(user_id, team_id):
    file_path = f"./data/installations/none-{team_id}/installer-{user_id}-latest"
    try:
        with open(file_path, 'r') as file:
            installation_data = json.load(file)
            return installation_data.get('user_token')
    except FileNotFoundError:
        logging.error(f"Installation file not found: {file_path}")
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file: {file_path}")
    return None

# Register command handlers
app.command("/upload")(command_handlers.open_modal)

# Register view submission handlers
@app.view("image_upload_modal")
def handle_image_upload(ack, body, client, context):
    ack()
    logging.info(json.dumps(body, indent=2))
    user_id = body["user"]["id"]
    team_id = body["team"]["id"]
    user_token = get_user_token(user_id, team_id)
    channel_id = body["view"]["state"]["values"]["channel_block_id"]["channel_select_action_id"]["selected_conversation"]
    file_info = body["view"]["state"]["values"]["input_block_id"]["file_input_action_id_1"]["files"][0]
    file_id = file_info["id"]
    file_url = file_info["url_private_download"]
    file_path = download_file(file_url, os.environ.get('SLACK_BOT_TOKEN'))
    encoded_image = encode_image_to_base64(file_path)
    delete_file(client, user_token, file_id)
    description = generate_image_description(encoded_image, os.environ.get('OLLAMA_API_URL'))
    upload_file(client, user_token, channel_id, description, file_path)

def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).connect()
    app.start(port=int(os.environ.get("PORT", 3000)))
