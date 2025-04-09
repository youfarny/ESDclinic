from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name__)

# RabbitMQ connection settings
RABBITMQ_HOST = 'localhost'  # RabbitMQ is running locally
QUEUE_NAME = 'sms_queue'

# Set up the RabbitMQ connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Ensure the queue exists
channel.queue_declare(queue=QUEUE_NAME)

@app.route('/send_sms', methods=['POST'])
def send_sms():
    # Get the data from the POST request
    data = request.get_json()

    # Ensure the request contains 'to' and 'body'
    if not data or 'to' not in data or 'body' not in data:
        return jsonify({"error": "Missing 'to' or 'body' in request"}), 400

    # Create a message to send to RabbitMQ
    message = json.dumps({
        'to': data['to'],
        'body': data['body']
    })

    # Send the message to the RabbitMQ queue
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=message
    )

    return jsonify({"status": "Message queued successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

