import base64
import json
import requests
from settings import *


def main(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')  # type: json
    log_data = json.loads(pubsub_message)  # type: dict
    print(log_data)

    log_name = log_data["logName"]  # type: str
    resource = log_data["resource"]["labels"]  # type: dict
    resource_data = ""  # type: str
    for key, value in resource.items():
        resource_data = resource_data + "{} : {}\n".format(key, value)

    log = log_data["textPayload"]  # type: str

    data = {  # type: dict
        "attachments": [
            {
                "color": "00ffff",
                "text": "*LogName*\n{}".format(log_name),
            },
            {
                "color": "00bfff",
                "text": "*ResourceInfo*\n{}".format(resource_data),
            },
            {
                "color": "4169e1",
                "text": "*LogInfo*\n{}".format(log)
            },
        ]
    }
    print(data)

    json_data = json.dumps(data).encode("utf-8")  # type: json
    response = requests.post(SLACK_WEBHOOK_URL, json_data)
    print(response)
    print(response.text)


if __name__ == '__main__':
    main("event", "context")
