import base64
import json
import requests
from settings import *


def main(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')  # type: json
    log_data = json.loads(pubsub_message)  # type: dict
    print(log_data)

    log_name = log_data["logName"]
    resource = log_data["resource"]["labels"]
    resource_data = ""
    for key, value in resource.items():
        resource_data = resource_data + "{} : {}\n".format(key, value)

    log = log_data["textPayload"]

    blocks_data = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*LogName*\n{}".format(log_name)
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*ResourceInfo*\n{}".format(resource_data)
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*LogInfo*\n{}".format(log)
            }
        },
    ]

    url = "https://slack.com/api/chat.postMessage"
    data = {
        "channel": CHANNEL_ID,
        "blocks": str(blocks_data),
    }
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + BOT_USER_OAUTH_TOKEN}

    json_data = json.dumps(data).encode("utf-8")
    response = requests.post(url, json_data, headers=headers)
    print(response)
    print(response.text)


if __name__ == '__main__':
    main("event", "context")
