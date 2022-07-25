import json
import time
import requests

import numpy as np

from pika_utils import Consumer


QUEUE_NAME = "processing_q_1"
URL = "http://api:8000/processing/update"


def callback(ch, method, properties, body):

    task = json.loads(body)

    print("\nProcessing ", task["uuid"], "...")

    output_data = process(task["process"])
    task["complete"] = True
    task["data"] = output_data

    json_data = json.dumps(task)

    response = requests.put(URL, data=json_data, headers={"Content-Type": "application/json"})
    print(response)

    print("Completed!")


def process(process_name: str) -> dict:
    # This is some time-consuming process...
    time.sleep(5)
    return {
        "values": list(np.random.rand(10)),
        "description": f"This data was created by {process_name} process."
    }


if __name__ == "__main__":

    consumer = Consumer()
    consumer.receive(QUEUE_NAME, callback)