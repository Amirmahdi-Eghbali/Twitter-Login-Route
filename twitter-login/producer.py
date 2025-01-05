import json
import uuid
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
                         )

def send_message(credentials):

    task_id = str(uuid.uuid4())
    message = {"task_id" : task_id, "credentials" : credentials.dict()}
    producer.send("twitter_login_requests", value=message)
    producer.flush()
    print("message sent")

    return task_id


