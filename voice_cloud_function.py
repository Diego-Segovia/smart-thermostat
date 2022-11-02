from dotenv import load_dotenv
import os
import json
from google.cloud import pubsub_v1

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")

def publish_messages(project_id, topic_id, payload):
    """Publishes multiple messages to a Pub/Sub topic."""

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    message_json = json.dumps(payload)
    data = message_json.encode('utf-8')
    publisher.publish(topic_path, data)
    print(f"Published messages to {topic_path}.")
    

def process_voice(request):
    print('Processing voice...')
    request_json = request.get_json()
    queryResult = request_json['queryResult']
    parameters = queryResult['parameters']

    power_cmd = parameters['powercmd']
    payload = {"powerStatus": power_cmd}
    publish_messages(PROJECT_ID, TOPIC_ID, json.dumps(payload))
