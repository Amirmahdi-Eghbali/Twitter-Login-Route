import bcrypt
from kafka import KafkaConsumer
from models import TaskStatus, UserCredentials as UC
import json

consumer = KafkaConsumer(
    "twitter_login_requests",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    enable_auto_commit=True,
    group_id="task-group"
)

async def consume_messages():
    for message in consumer:
        task_id = message.value['task_id']
        credentials = message.value['credentials']

        user = await UC.find_one({
            "username": credentials["username"],
            "phone_number": credentials["phone_number"]
        })

        if user and bcrypt.checkpw(credentials["password"].encode('utf-8'), user["password"].encode('utf-8')):
            status = "success"
        else:
            status = "failure"

        task_status = TaskStatus(task_id=task_id, status=status)
        try:
            print("start")
            await task_status.insert()
            print(f"task {task_id} processed with {status}")
        except Exception as e:
            print(f"couldn't save task {task_id} : {e}")