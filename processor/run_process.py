import json
import time
import requests

import numpy as np

from pika_utils import Consumer


QUEUE_NAME = "processing_q_1"
URL = "http://api:8000/processing/update"


def callback(ch, method, properties, body):
    """
    Callback function for RabbitMQ queue consumer. Takes the body of the message
    from the queue (a JSON POST request to the API by the user) and performs some
    data processing.
    The task is updated with the processed data and a PUT request is made to the API
    which then updates the task record in the database, allowing the user to access
    the results of the data processing.
    """

    task = json.loads(body)

    print("\nProcessing ", task["uuid"], "...")

    output_data = process(task["process"])
    task["complete"] = True
    task["data"] = output_data

    task_json = json.dumps(task)

    response = requests.put(URL, data=task_json, headers={"Content-Type": "application/json"})

    print(response)
    print("Completed!")


def process(process_name: str) -> dict:
    """
    An example of a data processing function, that produces some output
    data from the users original request.
    """
    
    time.sleep(10)
    return {
        "values": list(np.random.rand(10)),
        "description": f"This data was created by {process_name} process."
    }


def main():
    """
    Connect to the message queue and run the callback function on each new
    message that arrives.
    """
    
    consumer = Consumer()
    consumer.receive(QUEUE_NAME, callback)


if __name__ == "__main__":

    main()
