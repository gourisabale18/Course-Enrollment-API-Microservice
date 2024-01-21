#!/usr/bin/env python
import pika
import json
import httpx

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
    
    def _make_post_request(self, data):
        url = data.get("callback_url")
        section_id = data.get("section_id")

        try:
            httpx.post(url, json={"message": f"You have been enrolled in section {section_id}"})
        except httpx.RequestError as e:
            print(f"Request error: {e}")
        except httpx.HTTPError as e:
            print(f"HTTP error: {e}")

    def consume(self):
        def callback(ch, method, properties, body):
            data = json.loads(body)
            self._make_post_request(data)

            # print(f" [x] {data}")
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
    consumer = RabbitMQConsumer(queue_name='email')
    consumer.consume()
    consumer.start_consuming()
