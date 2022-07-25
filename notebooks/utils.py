import os
import sys
import pika


class Rabbit:
    host = "rabbit"
    port = 5672
    
    def connect(self):
        connection_params = pika.ConnectionParameters(Rabbit.host, Rabbit.port)
        return pika.BlockingConnection(connection_params)
    

class Producer(Rabbit):
    def send(self, queue_name, body):
        
        try:
            connection = self.connect()
            channel = connection.channel()
            channel.queue_declare(queue=queue_name)
            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=body
            )
        except Exception as e:
            raise e
        finally:
            connection.close()
    

class Consumer(Rabbit):
    def receive(self, queue_name):
        connection = self.connect()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.callback
        )

        try:
            print("Receiving")
            channel.start_consuming()
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    @staticmethod
    def callback(ch, method, properties, body):
        print(body)