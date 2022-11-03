'''Voice Processing Google Cloud Function
Cloud Function used to extract power command from DialogFlow voice request.
Python version: 3.7
Dependency: google-cloud-pubsub
Note: Change project id & topic id for explicit project info without using environment variables.
'''
from dotenv import load_dotenv # Not needed for Google Cloud
import os # Not needed for Google Cloud
import json
from google.cloud import pubsub_v1

load_dotenv() # Not needed for Google Cloud

PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")

def publish_messages(project_id, topic_id, payload):
    """Publishes multiple messages to a Pub/Sub topic."""

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    message_json = json.dumps(payload)
    data = message_json.encode('utf-8')
    publisher.publish(topic_path, data)
    

def process_voice(request):
    request_json = request.get_json()
    queryResult = request_json['queryResult']
    parameters = queryResult['parameters']

    power_cmd = parameters['powerstatus']
    payload = {"powerStatus": power_cmd}
    publish_messages(PROJECT_ID, TOPIC_ID, json.dumps(payload))
