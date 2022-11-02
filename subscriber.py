from dotenv import load_dotenv
import os
import json
from google.cloud import pubsub_v1

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")
SUBSCRIPTION_NAME = os.getenv("SUBSCRIPTION_NAME")

credentials_path = './smart_thermostat_private_key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

subscription_name = f'projects/{PROJECT_ID}/subscriptions/{SUBSCRIPTION_NAME}'

subscriber = pubsub_v1.SubscriberClient()


def callback(message):
    data = message.data
    power_command = json.loads(data)
    power_cmd = power_command.split(":")[1].split("}")[0].split('"')[1].split('"')[0]
    print(f"Thermostat Power Command: {power_cmd}.")
    message.ack()

future = subscriber.subscribe(subscription_name, callback=callback)
print(f'Listening on {subscription_name}')

with subscriber:
    try:
        future.result()
    except:
        future.cancel()
        future.result()
    

