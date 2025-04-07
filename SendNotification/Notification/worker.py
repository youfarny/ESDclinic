import pika
import json
from twilio.rest import Client


# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACe92d9c480a20df1a8041c53f7ac1992a'
TWILIO_AUTH_TOKEN = '1feee1b9abaf98512122a2fb10fdfd92'
TWILIO_PHONE_NUMBER = '+12723155371'

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# RabbitMQ settings
RABBITMQ_HOST = '116.15.73.191'  # Your on-prem RabbitMQ IP
RABBITMQ_PORT = 5672  # AMQP port
QUEUE_NAME = 'sms_queue'

# Set up the RabbitMQ connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    credentials=pika.PlainCredentials('admin', 'ESD213password!')
))
channel = connection.channel()

# Declare the queue (it should match the one in Flask)
channel.queue_declare(queue=QUEUE_NAME)

def callback(ch, method, properties, body):
    # Decode the message
    message = json.loads(body)
    to = message['to']
    body = message['body']

    # Send the SMS via Twilio
    try:
        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=to
        )
        print(f"Message sent to {to}: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")

# Set up the worker to consume messages from the queue
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

# Start consuming messages
print('Worker is waiting for messages. To exit press CTRL+C')
channel.start_consuming()

