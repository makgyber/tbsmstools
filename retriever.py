import os
import requests

from dotenv import load_dotenv

from utils import put_message_to_queue


def sync_messages():
    # retrieve from remote server
    messages = retrieve_messages()
    # save messages to queue
    save_to_queue(messages)
    # trigger delete from remote server
    send_delete()


def retrieve_messages():
    api_url = os.environ.get("SMS_MESSAGE_SERVER_URL")
    verify = os.environ.get("VERIFY_CERT") == "True"
    response = requests.get(api_url, verify=verify)
    messages = response.json()
    return messages


def save_to_queue(messages):
    for idx, message in enumerate(messages):
        filename = message["name"].replace(" ", "_")
        phone = (
            message["to"]
            if message["to"].startswith("+")
            else message["to"].replace("0", "+63")
        )
        put_message_to_queue(message=message["message"], to=phone, filename=filename)


def send_delete():
    pass


if __name__ == "__main__":
    load_dotenv(".env")
    sync_messages()
