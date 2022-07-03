#! /usr/bin/python3
# -*- coding: utf-8 -*-
import os
# Use the package we installed
from slack_bolt import App, Say

import datetime
import requests
import codecs
import re
import urllib.request
import json

from callback_blocks import one_file_blocks, two_file_blocks
from cloud_api import upload_file

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# [
#    thread_ts:,
#    user_id:,
#    author:,
#    title:,
#    date:,
#    files : {
#        file_name : {
#           id:,
#           download_url:
#           type: seminar_presentation/seminar_handout/rinko_textbok/rinko_ex/ppaper_intro
#        },
#    },
#    feedback:,
# ]
#
db = []


@app.event("message")
def handle_message_events(event, logger, client, body, say):
    if event.get("files") is None:
        return

    for file in event["files"]:
        if file["filetype"] != "pdf":
            client.chat_postMessage(
                text="Only PDF file for our database",
                channel=event["channel"],
                thread_ts=event["ts"],
            )
            return

    message_db = {
        "thread_ts": event["thread_ts"] if "thread_ts" in event else event["event_ts"],
        "user_id" : event["user"],
        "author" : client.users_profile_get(user=event["user"])["profile"]["real_name"],
        "title" : None,
        "date" : datetime.date.fromtimestamp(int(float(event["ts"]))),
        "files": {},
        "feedback" : None,
    }

    for file in event["files"]:
        file_name = file.get("name")
        id = file.get("id")
        message_db["files"][file_name] = {"id":id, "download_url":file.get("url_private_download"), "type":None}

        ## download using files_sharedPublicURL
        # response = client.files_sharedPublicURL(token=os.environ.get("SLACK_API_TOKEN"), file=id)
        # permalink_public = response["file"]["permalink_public"]
        # url_content = requests.get(permalink_public).text
        # pattern = re.compile(r"https://[-_./a-zA-Z0-9]+\.pdf\?pub_secret=[a-zA-Z0-9]+")
        # download_url = pattern.search(url_content).group()
        # print(file.get("url_private_download"))

    blocks = two_file_blocks(message_db.get("author"), message_db.get("date"), [key for key in message_db["files"].keys()])
    try:
        client.chat_postMessage(
            text="",
            channel=event["channel"],
            thread_ts=event["ts"],
            blocks=blocks,
        )

    except Exception as e:
        logger.error(f"Error publishing reply: {e}")


    db.append(message_db)


@app.action("approve_action")
def confirm_action_callback(ack, body, logger, client):
    ack()

    target_db = None
    for data in db:
        if data.get("thread_ts") == body["container"]["thread_ts"] and data.get("user_id") == body["user"]["id"]:
            target_db = data

    if target_db is None:
        logger.info("cannot mach user")
        return

    values = body["state"]["values"]
    target_db["author"] = values["author"]["author-action"]["value"]
    target_db["title"] = values["title"]["title-action"]["value"]
    target_db["date"] = values["date"]["date-action"]["selected_date"]

    for file_name in target_db["files"].keys():
        target_db["files"][file_name]["type"] = values[f"document_type_{file_name}"]["document_type-action"]["selected_option"]["value"]

    try:
        client.chat_delete(
         channel=body["container"]["channel_id"],
         ts=body["container"]["message_ts"],
        )

    except Exception as e:
         logger.error(f"Error deleting bot message: {e}")

    for file_name, file_data in target_db["files"].items():
        download_name = f"tmp/{file_name}"
        dir_name = f"{target_db['date']}_{target_db['author']}"
        name = f"{target_db['date']}_{target_db['author']}_{file_data['type']}"
        download_file(file_data["download_url"], download_name, os.environ.get("SLACK_BOT_TOKEN"))
        upload_file(download_name, name, dir_name, "pdf")

    metadata_file = f"tmp/{date}_{author}.json"
    json_obj = open(metadata_file, mode="w")
    json.dump(target_db, json_obj)
    json_obj.close()
    upload_file(metadata_file, f"{date}_{author}.json", dir_name, "metadata")


@app.action("deny_action")
def confirm_action_callback(ack, body, client):
    ack()
    try:
        client.chat_delete(
            channel=body["container"]["channel_id"],
            ts=body["container"]["message_ts"],
        )
        # [todo] delete database

    except Exception as e:
        logger.error(f"Error deleting bot message: {e}")


def download_file(url, file_name, bot_token):
    ## download using url_private_donwload
    content = requests.get(
        url,
        allow_redirects=True,
        headers={"Authorization" : f"Bearer {bot_token}"},
        stream=True,
        ).content
    target_file = codecs.open(file_name, "wb")
    target_file.write(content)
    target_file.close()


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
