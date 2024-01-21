#!/usr/bin/env python
import pika
import json

class RabbitMQConsumer:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.channel = self.setup_rabbitmq()

    def setup_rabbitmq(self):
        # Establish a connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # Declare queues and exchanges
        channel.queue_declare(queue='email', durable=True)
        channel.queue_declare(queue='webhook', durable=True)

        channel.exchange_declare(exchange='notification', exchange_type='fanout')

        # Bind queues to the fanout exchange
        channel.queue_bind(exchange='notification', queue='email')
        channel.queue_bind(exchange='notification', queue='webhook')

        # print(' [*] Waiting for logs. To exit press CTRL+C')

        return channel

    def consume(self):
        def callback(ch, method, properties, body):
            message = json.loads(body)
            # print(f" [x] {message}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=False)
        # print(f' [*] Waiting for messages on queue: {self.queue_name}. To exit press CTRL+C')

    def start_consuming(self):
        try:
            # Start consuming messages indefinitely
            self.channel.start_consuming()
        except KeyboardInterrupt:
            # Handle interruption (Ctrl+C)
            # print(" [*] Stopped consuming messages.")
            self.channel.stop_consuming()

if __name__ == "__main__":
    # Example usage
    consumer = RabbitMQConsumer(queue_name='webhook')
    consumer.consume()
    consumer.start_consuming()
