from dotenv import load_dotenv
from google.cloud import pubsub_v1
import os
import json
import publisher
import re

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
    message.ack()
    
    # Formatting data bytestring for JSON parsing
    power_cmd_data = data.decode('utf-8').replace(" ", "").replace("\\", "")
    power_cmd_data = re.sub(r'^.', "", power_cmd_data)
    power_cmd_data = re.sub(r".$", "", power_cmd_data)

    power_cmd = json.loads(power_cmd_data)['powerStatus']
    print(f'PubSub Command: {power_cmd}')
    publisher.add_power_cmd(power_cmd)
    publisher.execute_command()

future = subscriber.subscribe(subscription_name, callback=callback)
print(f'Listening on subscriptions/{SUBSCRIPTION_NAME}')

with subscriber:
    try:
        future.result()
    except:
        future.cancel() # Trigger receiver processing shutdown.
        future.result() # Block until shutdown complete.
    

