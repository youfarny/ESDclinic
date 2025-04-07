from flask import Flask, request, jsonify
import pika
import json
from twilio.rest import Client
import threading

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
QUEUE_NAME = 'sms_queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    credentials=pika.PlainCredentials('admin', 'ESD213password!')
))

channel = connection.channel()
channel.queue_declare(queue='sms_queue')

def craft_message(appointment_type, patient_contact, queue_length=None, payment_amount=None):
    if appointment_type == 'before':
        # Craft the message for before the appointment
        message = f"Dear Patient, your appointment is coming up soon! Estimated wait time: {queue_length} patients ahead. Please be ready."
    
    elif appointment_type == 'during':
        # Craft the message for during the appointment
        message = "Thank you for waiting. Your doctor is available to see you now, please enter the virtual meeting room via our application."
    
    elif appointment_type == 'after':
        # Craft the message for after the appointment
        message = f"Thank you for visiting! Your total payment is {payment_amount} USD. Please settle it at your earliest convenience."
    
    else:
        message = "Invalid appointment type."

    return message

# Callback function to consume messages from RabbitMQ
def callback(ch, method, properties, body):
    # Decode the message
    message_data = json.loads(body)
    
    # Extract the variables from the message
    appointment_type = message_data['appointment_type']
    patient_contact = message_data['patient_contact']
    queue_length = message_data.get('queue_length', None)
    payment_amount = message_data.get('payment_amount', None)
    
    # Craft the message based on the appointment type
    message = craft_message(appointment_type, patient_contact, queue_length, payment_amount)
    
    # Send the message via Twilio
    try:
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=patient_contact
        )
        print(f"Message sent to {patient_contact}: {msg.sid}")
    except Exception as e:
        print(f"Failed to send message to {patient_contact}: {e}")
    
    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consuming():
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)
    print("Worker is waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

# Start the RabbitMQ consumer in a new thread
def start_rabbitmq_consumer():
    consumer_thread = threading.Thread(target=start_consuming)
    consumer_thread.daemon = True  # Daemon thread will exit when the main program exits
    consumer_thread.start()

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
    # Start consuming messages from the queue
#channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

print("Worker is waiting for messages. To exit press CTRL+C")
#channel.start_consuming()

if __name__ == 'main':
    start_rabbitmq_consumer()
    app.run(debug=True, host='0.0.0.0')


