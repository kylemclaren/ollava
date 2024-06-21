def open_modal(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "image_upload_modal",
            "title": {"type": "plain_text", "text": "Upload Image"},
            "submit": {"type": "plain_text", "text": "Submit"},  # Submit button
            "blocks": [
                {
                    "type": "input",
                    "block_id": "input_block_id",
                    "label": {"type": "plain_text", "text": "Upload Files"},
                    "element": {
                        "type": "file_input",
                        "action_id": "file_input_action_id_1",
                        "filetypes": ["jpg", "png"],
                        "max_files": 1,
                    },
                },
                {
                    "type": "input",
                    "block_id": "channel_block_id",
                    "label": {"type": "plain_text", "text": "Select Channel"},
                    "element": {
                        "type": "conversations_select",
                        "action_id": "channel_select_action_id",
                        "default_to_current_conversation": True,
                        "placeholder": {"type": "plain_text", "text": "Select a channel"},
                    },
                },
            ],
        },
    )
