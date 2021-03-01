import base64
import json


def main(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    # JSON形式の文字列を辞書に変換
    d = json.loads(pubsub_message)
    print(d)


if __name__ == '__main__':
    main("event", "context")
