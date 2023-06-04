import firebase_admin
from firebase_admin import credentials, messaging

firebase_cred = credentials.Certificate("firebase.json")
firebase_app = firebase_admin.initialize_app(firebase_cred)


# Subscribe to a topic
def subscribe_news(tokens):  # tokens is a list of registration tokens
    topic = 'news'
    response = messaging.subscribe_to_topic(tokens, topic)
    if response.failure_count > 0:
        print(f'Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason, response.errors))}')


# Unsubscribe from a topic
def unsubscribe_news(tokens):  # tokens is a list of registration tokens
    topic = 'news'
    response = messaging.unsubscribe_from_topic(tokens, topic)
    if response.failure_count > 0:
        print(f'Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason, response.errors))}')


# Send push notification to a topic
def send_topic_push(title, body):
    topic = 'news'
    message = messaging.Message(
        notification=messaging.Notification(title=title,body=body),
        topic=topic
    )
    messaging.send(message)


# Send push notification to multiple tokens
def send_token_push(title, body, tokens):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        tokens=tokens
    )
    messaging.send_multicast(message)
