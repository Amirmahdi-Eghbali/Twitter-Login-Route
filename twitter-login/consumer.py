import asyncio
import time
import bcrypt
import json
from kafka import KafkaConsumer
from models import TaskStatus, UserCredentials as UC

consumer = KafkaConsumer(
    "twitter_login_requests",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    enable_auto_commit=True,
    group_id="task-group",
    consumer_timeout_ms=5000
)


async def consume_messages():
    last_message = time.time()
    try:
        while True:
            messages = consumer.poll(timeout_ms=1000)
            if not messages:
                if time.time() - last_message > 6:
                    print("No new messages.")
                    await asyncio.sleep(6)
                    continue

            for temp, msgs in messages.items():
                for message in msgs:
                    last_message = time.time()
                    try:
                        task_id = message.value['task_id']
                        credentials = message.value['credentials']

                        user = await UC.find_one({
                            "username": credentials["username"],
                            "phone_number": credentials["phone_number"]
                        })
                        if user:
                            print(user.password.encode('utf-8'))
                            print(credentials["password"])
                        if user and bcrypt.checkpw(credentials["password"].encode('utf-8'),
                                                   user.password.encode('utf-8')):
                            status = "success"
                        else:
                            status = "failure"

                        task_status = TaskStatus(task_id=task_id, status=status)
                        await task_status.insert()
                        print(f"Task {task_id} processed with status: {status}")

                    except Exception as e:
                        print(f"Error processing message: {e}")

    except Exception as e:
        print(f"Consumer error: {e}")
    finally:
        consumer.close()