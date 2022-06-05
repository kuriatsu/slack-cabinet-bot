import os
# Use the package we installed
from slack_bolt import App, Say
import datetime
import requests
import codecs
import re
# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# ts: {
#    files : {
#       filename:{
#           id:,
#           download_url:
#           type: powerpoint/handout
#        },
#    },
#    type: [],
#    author:,
#    title:,
#    date:,
# }
#
temp_db = {}


@app.event("message")
def handle_message_events(event, logger, client, body, say):
    if event.get("files") is None:
        return

    for file in event["files"]:
        # print(file["filetype"])
        if file["filetype"] != "pdf":
            client.chat_postMessage(
                text="Only PDF file for our database",
                channel=event["channel"],
                thread_ts=event["ts"],
            )
            return

    user_name = client.users_profile_get(user=event["user"])["profile"]["real_name"]
    date = datetime.date.fromtimestamp(int(float(event["ts"])))
    # print(event["ts"])
    message_db = {
        "files": {},
        "type" : None,
        "author" : user_name,
        "title" : None,
        "date" : date
    }

    for file in event["files"]:
        filename = file.get("name")
        id = file.get("id")
        response = client.files_sharedPublicURL(token=os.environ.get("SLACK_API_TOKEN"), file=id)
        permalink_public = response["file"]["permalink_public"]
        url_content = requests.get(permalink_public).text
        pattern = re.compile(r"https://[-_./a-zA-Z0-9]+\.pdf\?pub_secret=[a-zA-Z0-9]+")
        download_url = pattern.search(url_content).group()

        message_db["files"][filename] = {"id":id, "download_url":download_url, "type":None}

    temp_db[event["ts"]] = message_db

    if len(message_db["files"]) == 1:
        blocks = [
        {
            "type": "input",
            "block_id" : "document_type",
            "element": {
                "type": "static_select",
                "action_id": "document_type-action",
				"initial_option": {
					"text": {
						"type": "plain_text",
						"text": "Seminar Presentation",
						"emoji": True
					},
					"value": "seminar_presentation"
				},
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Seminar Presentation",
                            "emoji": True
                        },
                        "value": "seminar_presentation"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Seminar Handout",
                            "emoji": True
                        },
                        "value": "seminar_handout"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "輪講",
                            "emoji": True
                        },
                        "value": "rinko"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "輪講 Excercise",
                            "emoji": True
                        },
                        "value": "rinko_ex"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Paper Introduction",
                            "emoji": True
                        },
                        "value": "paper_intro"
                    }
                ]
            },
            "label": {
                "type": "plain_text",
                "text": "Type",
                "emoji": True
            }
        },
        {
            "type": "input",
            "block_id" : "title",
            "element": {
                "type": "plain_text_input",
                "action_id": "title-action",
            },
            "label": {
                "type": "plain_text",
                "text": "Title",
                "emoji": True
            }
        },
        {
            "type": "input",
            "block_id" : "author",
            "element": {
                "type": "plain_text_input",
                "action_id": "author-action",
                "initial_value": user_name,
            },
            "label": {
                "type": "plain_text",
                "text": "Author",
                "emoji": True
            }
        },
        {
            "type": "input",
            "block_id" : "date",
            "element": {
                "type": "datepicker",
                "action_id": "date-action",
                "initial_date": str(date),
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": True
                },
            },
            "label": {
                "type": "plain_text",
                "text": "Date",
                "emoji": True
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Approve"
                    },
                    "style": "primary",
                    "value": "approve",
                    "action_id": "approve_action",
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Deny"
                    },
                    "style": "danger",
                    "value": "deny",
                    "action_id": "deny_action"
                }
            ]
        }]

    try:
        client.chat_postMessage(
            text="",
            channel=event["channel"],
            thread_ts=event["ts"],
            blocks=blocks,
        )

    except Exception as e:
        logger.error(f"Error publishing reply: {e}")


@app.action("approve_action")
def confirm_action_callback(ack, body):
    ack()
    values = body["state"]["values"]
    type = values["document_type"]["document_type-action"]["selected_option"]["value"]
    author = values["author"]["author-action"]["value"]
    title = values["title"]["title-action"]["value"]
    date = values["date"]["date-action"]["selected_date"]
    # print(body["container"]["thread_ts"])
    # print(type, author, title, date)

    temp_db[body["container"]["thread_ts"]]["type"] = type
    temp_db[body["container"]["thread_ts"]]["author"] = author
    temp_db[body["container"]["thread_ts"]]["title"] = title
    temp_db[body["container"]["thread_ts"]]["date"] = date

    # try:
    #     client.chat_delete(
    #         channel=body["container"]["channel_id"],
    #         ts=body["container"]["message_ts"],
    #     )
    #
    # except Exception as e:
    #     logger.error(f"Error deleting bot message: {e}")


@app.action("deny_action")
def confirm_action_callback(ack, body, client):
    ack()
    try:
        client.chat_delete(
            channel=body["container"]["channel_id"],
            ts=body["container"]["message_ts"],
        )

    except Exception as e:
        logger.error(f"Error deleting bot message: {e}")



# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
