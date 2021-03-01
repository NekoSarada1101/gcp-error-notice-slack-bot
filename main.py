import base64
import json
import requests
from datetime import datetime, timedelta
from settings import *


def main(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')  # type: json
    # JSON形式の文字列を辞書に変換
    log_data = json.loads(pubsub_message)  # type: dict
    print(log_data)

    log_name = log_data["logName"]
    time = (datetime.strptime("2021-03-01T08:58:17.29752278Z"[0:19],
                              '%Y-%m-%dT%H:%M:%S') + timedelta(hours=9)).strftime(
        '%Y/%m/%d %H:%M:%S')
    log = log_data["textPayload"]

    blocks_data = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "{}\n*{}*".format(time, log_name)
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*ログ情報*\n{}".format(log)
            }
        },
    ]

    url = "https://slack.com/api/chat.postMessage"
    data = {
        "channel": CHANNEL_ID,
        "username": "GCP Error",
        "icon_emoji": ":googlecloud:",
        "blocks": blocks_data,
    }
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + BOT_USER_OAUTH_TOKEN}

    json_data = json.dumps(data).encode("utf-8")
    response = requests.post(url, json_data, headers=headers)
    print(response)


if __name__ == '__main__':
    main("event", "context")
