import firebase_admin
from firebase_admin import credentials, messaging
import json

cred = credentials.Certificate("config/todofuken-crawler-firebase-adminsdk-fbsvc-2722d157c4.json")
firebase_admin.initialize_app(cred)

def send_push(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
    )
    response = messaging.send(message)
    print("Sent:", response)


def send_all(title, body):
    with open("config/fcm_tokens.json", "r") as f:
        tokens = json.load(f)

    for tok in tokens:
        send_push(tok, title, body)