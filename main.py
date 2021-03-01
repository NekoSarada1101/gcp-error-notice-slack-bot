import base64
import json
from datetime import timedelta


def main(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')  # type: json
    # JSON形式の文字列を辞書に変換
    log_data = json.loads(pubsub_message)  # type: dict
    print(log_data)

    log_name = log_data["logName"]
    time = (log_name["receiveTimestamp"] + timedelta(hours=9)).strftime("%m/%d %H:%M:%s")
    log = log_data["textPayload"]

if __name__ == '__main__':
    main("event", "context")
