import json
import uuid

from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda r: json.dumps(r).encode("utf-8")
                         )

def send_message(login_request):

    task_id = str(uuid.uuid4())
    message = {"task_id" : task_id, "login_request" : login_request}

    producer.send("twitter-login-request", value=message)
    producer.flush()

    return task_id


