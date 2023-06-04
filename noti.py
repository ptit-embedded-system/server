import firebase_admin
import client
from firebase_admin import credentials, messaging

import config


class Firebase:
    def __init__(self):
        self.default_topic = "ptit-iot"
        self.redis_cli = client.RedisClient()
        self.firebase_cred = credentials.Certificate("config/account-cert.json")
        self.firebase_app = firebase_admin.initialize_app(self.firebase_cred)

    # Subscribe to a topic

    def subscribe_news(self, tokens, topic):  # tokens is a list of registration tokens
        topic = self.default_topic if topic is None else topic
        self.redis_cli.set(tokens, topic)
        response = messaging.subscribe_to_topic(tokens, topic)
        if response.failure_count > 0:
            print(f'Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason, response.errors))}')

    # Unsubscribe from a topic
    def unsubscribe_news(self, tokens, topic):  # tokens is a list of registration tokens
        topic = self.default_topic if topic is None else topic
        response = messaging.unsubscribe_from_topic(tokens, topic)
        if response.failure_count > 0:
            print(f'Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason, response.errors))}')

    # Send push notification to a topic
    def send_topic_push(self, title, body, topic):
        topic = self.default_topic if topic is None else topic
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            topic=topic
        )
        messaging.send(message)

    # Send push notification to multiple tokens

    def send_token_push(self, title, body, tokens):
        val = self.redis_cli.get(tokens)
        if val is None:
            return
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            tokens=tokens
        )
        messaging.send_multicast(message)

    def push_all_device(self, title, body):
        keys = self.redis_cli.keys()
        for key in keys:
            # print(key, end='\n')
            self.send_token_push(title=title, body=body, tokens=key)


if __name__ == "__main__":
    firebase = Firebase()
    # firebase.subscribe_news(topic=None,
    #                         tokens="dEOldzg-T7mYxhXDdk5aol:APA91bESf8qqu3GUkosMAOkal5yaF3zSBK8-LkbemoS_rnu9yZZVac_2O850pc9cU4hHErAEhVn5oEaDD5D1IEt8qw-qb9i58GuYfO8hw7VGGpZNPwsVZHcFuDA9mcCIZBXfCFcXR9DD")
    # firebase.send_topic_push("test noti", "Test noti", topic=None)
    firebase.push_all_device("test noti", "test")
