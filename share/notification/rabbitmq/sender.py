import pika
import json
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv


class RabbitManager:
    def __init__(self, host='localhost'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        # Declare queues and exchanges
        self.channel.queue_declare(queue='email', durable=True)
        self.channel.queue_declare(queue='webhook', durable=True)

        self.channel.exchange_declare(exchange='notification', exchange_type='fanout')

        # Bind queues to the fanout exchange
        self.channel.queue_bind(exchange='notification', queue='email')
        self.channel.queue_bind(exchange='notification', queue='webhook')

    def publish_notification(self, notification_details):
        # Publish a notification
        self.channel.basic_publish(
            exchange='notification',
            routing_key='',
            body=json.dumps(notification_details),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

        # Automatically close the connection after publishing
        self.connection.close()

    def publish_email(self, notification_details):
        sender_email = 'notifications@gmail.com'
        recipient_email = notification_details.get('email')
        section_id = notification_details.get('section_id')

        subject = 'You have been enrolled!'
        body = f"Congratulations, you have been enrolled in section {section_id}"

        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient_email

        try:
            # Connect to the local aiosmtpd server
            with smtplib.SMTP('localhost', 8025) as server:
                # Send the email
                server.sendmail(sender_email, recipient_email, message.as_string())

            print("Email sent successfully!")

        except Exception as e:
            print(f"Failed to send email. Error: {e}")