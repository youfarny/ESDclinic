from flask import Flask, request, jsonify
import pika
import json
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACe92d9c480a20df1a8041c53f7ac1992a'
TWILIO_AUTH_TOKEN = '1feee1b9abaf98512122a2fb10fdfd92'
TWILIO_PHONE_NUMBER = '+12723155371'

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# RabbitMQ Connection
RABBITMQ_HOST = '116.15.73.191'  # Your on-prem RabbitMQ IP
RABBITMQ_PORT = 5672  # AMQP port

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    credentials=pika.PlainCredentials('admin', 'ESD213password!')
))

channel = connection.channel()
channel.queue_declare(queue='sms_queue')


@app.route('/send_notification', methods=['POST'])
def send_notification():
    # Get the data from the POST request
    data = request.get_json()

    if not data or 'to' not in data or 'body' not in data:
        return jsonify({"error": "Missing 'to' or 'body' in request"}), 400

    # Format message for RabbitMQ
    message = json.dumps({
        'to': data['to'],
        'body': data['body'],
    })

    # Send the message to RabbitMQ
    channel.basic_publish(
        exchange='',
        routing_key='sms_queue',
        body=message
    )

    return jsonify({"status": "Notification message queued successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

