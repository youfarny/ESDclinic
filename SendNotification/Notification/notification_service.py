from flask import Flask, request, jsonify
import pika
import json
from twilio.rest import Client
import threading
from invokes import invoke_http
import requests


#Queue logic
def create_appointment_and_get_queue_length(doctor_id, patient_contact,appointment_id):
    queue_url = "http://116.15.73.191:5103/queue"  

    # Prepare the data to send to the Queue service
    data = {
        "doctor_id": doctor_id,
        "patient_contact": patient_contact,
        "appointment_id": appointment_id
    }

    # Send the POST request to create a new appointment and get the queue length
    response = requests.post(queue_url, json=data)

    if response.status_code == 201:
        # Successfully created the appointment and got the queue length
        response_data = response.json()
        queue_length = response_data.get("queue_length")
        return queue_length
    else:
        # Handle error
        print(f"Failed to create appointment: {response.text}")
        return None


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
QUEUE_NAME = 'notification_queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    credentials=pika.PlainCredentials('admin', 'ESD213password!')
))

channel = connection.channel()
channel.queue_declare(queue='notification_queue', durable=True)

# Declare the exchange (type can be 'direct', 'topic', etc. — adjust as needed)
channel.exchange_declare(exchange='esd_clinic', exchange_type='topic', durable=True)

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

    # Extract message info
    doctor_id = message_data.get('doctor_id')
    appointment_type = message_data.get('appointment_type')
    appointment_id = message_data.get('appointment_id')
    contact = message_data.get('patient_contact')
    patient_contact = "+65" + contact
    payment_amount = message_data.get('payment_amount', None)

    queue_length = create_appointment_and_get_queue_length(doctor_id, patient_contact,appointment_id)
    

    # Craft the outgoing message
    message = craft_message(appointment_type, patient_contact, queue_length, payment_amount)

    # Send the message via Twilio
    try:
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=patient_contact
        )
        print(f"Message sent to {patient_contact}: {msg.sid}")
        # You can use this if you want to return it as part of the response:
        response_payload = {
            "queue_length": queue_length or 3,  # Replace with real logic if needed
            "message_sid": msg.sid,
            "status": "sent"
        }

    except Exception as e:
        print(f"Failed to send message to {patient_contact}: {e}")
        response_payload = {
            "error": str(e),
            "status": "failed"
        }

    # Send response if reply_to and correlation_id are set
    if properties.reply_to and properties.correlation_id:
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id,
                content_type='application/json'
            ),
            body=json.dumps(response_payload)
        )
        print(f"✔ Sent response back to {properties.reply_to}")

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
        exchange='esd_clinic',
        routing_key='sms',
        body=message
    )

    return jsonify({"status": "Notification message queued successfully"}), 200
    # Start consuming messages from the queue
#channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

print("Worker is waiting for messages. To exit press CTRL+C")
#channel.start_consuming()

if __name__ == '__main__':
    start_rabbitmq_consumer()
    app.run(debug=True, host='0.0.0.0')


