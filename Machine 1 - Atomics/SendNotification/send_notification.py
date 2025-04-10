from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pika
import sys, os

import amqp_lib
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

from os import environ

# Get the IP address from an environment variable, defaulting to "116.15.73.191" if not set
ip_address = environ.get("IP_ADDRESS", "202.166.134.237")

# Define URLs using the IP address from the environment variable
appointment_URL = f"http://{ip_address}:5000/appointment"
#doctor_URL = f"http://{ip_address}:5001/doctor"
patient_URL = f"http://{ip_address}:5002/patient"
notification_URL = f"http://{ip_address}:5003/notification"
error_URL = f"http://{ip_address}:5006/error"

# RabbitMQ configuration
rabbit_host = ip_address
rabbit_port = 5672
exchange_name = "notification_topic"
exchange_type = "topic"

connection = None 
channel = None

def connectAMQP():
    # Use global variables to reduce number of reconnection to RabbitMQ
    global connection
    global channel

    print("  Connecting to AMQP broker...")
    try:
        connection, channel = amqp_lib.connect(
                hostname=rabbit_host,
                port=rabbit_port,
                exchange_name=exchange_name,
                exchange_type=exchange_type,
        )
        # Ensure the exchange is declared
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
        print("  Successfully connected to RabbitMQ.")
    except Exception as exception:
        print(f"  Unable to connect to RabbitMQ.\n     {exception=}\n")
        exit(1) # terminate


def get_rabbitmq_channel():
    """Return the RabbitMQ channel, reconnecting if necessary."""
    global connection, channel
    if connection is None or not amqp_lib.is_connection_open(connection):
        connectAMQP()
    return channel

@app.route("/send_notification", methods=['POST'])
def send_notification():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            notification_data = request.get_json()
            print("\nReceived a notification request in JSON:", notification_data)

            # Process the notification
            result = processNotification(notification_data)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print("Error: {}".format(ex_str))

            return jsonify({
                "code": 500,
                "message": "send_notification.py internal error:",
                "exception": ex_str,
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processNotification(notification_data):
    if connection is None or not amqp_lib.is_connection_open(connection):
        connectAMQP()
    channel = get_rabbitmq_channel()
    notification_type = notification_data.get("notification_type", "general")
    
    # Check if we need to fetch additional data based on notification type
    if notification_type == "appointment_confirmation" and "appointment_id" in notification_data:
        # Get appointment details
        print("  Invoking appointment microservice to get details...")
        appointment_result = invoke_http(
            appointment_URL + "/" + str(notification_data["appointment_id"]), 
            method="GET"
        )
        print(f"  appointment_result: {appointment_result}\n")
        
        if appointment_result["code"] not in range(200, 300):
            error_message = json.dumps({
                "code": 400,
                "data": appointment_result,
                "message": "Failed to retrieve appointment details for notification."
            })
            
            # Publish error via RabbitMQ
            print("  Publish message with routing_key=notification.error\n")
            channel.basic_publish(
                exchange=exchange_name,
                routing_key="notification.error",
                body=error_message,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            
            return {
                "code": 400,
                "data": {"appointment_result": appointment_result},
                "message": "Failed to retrieve appointment details for notification."
            }
        
        # Enhance notification with appointment details
        notification_data["appointment_details"] = appointment_result["data"]
        
        # Get patient contact information if not provided
        if "patient_contact" not in notification_data and "patient_id" in appointment_result["data"]:
            print("  Invoking patient microservice to get contact details...")
            patient_result = invoke_http(
                patient_URL + "/" + str(appointment_result["data"]["patient_id"]),
                method="GET"
            )
            print(f"  patient_result: {patient_result}\n")
            
            if patient_result["code"] in range(200, 300):
                notification_data["patient_contact"] = patient_result["data"].get("contact", "")
                notification_data["patient_name"] = patient_result["data"].get("name", "")
                notification_data["queue_length"] = appointment_result["data"].get("queue_length", 0)
    
    elif notification_type == "prescription_ready" and "prescription_id" in notification_data:
        # Here you would get prescription details if needed
        pass
    
    elif notification_type == "doctor_message" and "doctor_id" in notification_data:
        # Get doctor details
        print("  Invoking doctor microservice to get details...")
        doctor_result = invoke_http(
            f'https://personal-73tajzpf.outsystemscloud.com/Doctor_service/rest/DoctorAPI/doctor/byid?doctor_id={str(notification_data["doctor_id"])}', 
            method="GET")
           
        # print("  Invoking doctor microservice to get details...")
        # doctor_result = invoke_http(
        #     doctor_URL + "/" + str(notification_data["doctor_id"]),
        #     method="GET"
        # )
        print(f"  doctor_result: {doctor_result}\n")
        
        if doctor_result["code"] in range(200, 300):
            notification_data["doctor_name"] = doctor_result["data"].get("name", "")
    
    # Build message content if not provided
    if "message" not in notification_data:
        if notification_type == "appointment_confirmation":
            appointment_details = notification_data.get("appointment_details", {})
            notification_data["message"] = (
                f"Dear {notification_data.get('patient_name', 'Patient')}, "
                f"Your appointment #{appointment_details.get('appointment_id', 'N/A')} has been confirmed. "
                f"Queue length: {notification_data.get('queue_length', 'N/A')}. "
                f"Date: {appointment_details.get('date', 'N/A')}, "
                f"Time: {appointment_details.get('time', 'N/A')}."
            )
        elif notification_type == "prescription_ready":
            notification_data["message"] = "Your prescription is ready for pickup."
        elif notification_type == "doctor_message":
            notification_data["message"] = (
                f"Message from Dr. {notification_data.get('doctor_name', 'your doctor')}: "
                f"{notification_data.get('content', 'Please contact the clinic.')}"
            )
    
    # Send the notification
    print("  Invoking notification microservice...")
    notification_result = invoke_http(notification_URL, method="POST", json=notification_data)
    print(f"  notification_result: {notification_result}\n")
    
    # Prepare message for RabbitMQ
    notification_message = json.dumps(notification_result)
    
    # Check notification result and publish accordingly
    if notification_result["code"] in range(200, 300):
        # Log successful notification
        print("  Publish message with routing_key=notification.sent\n")
        channel.basic_publish(
            exchange=exchange_name, 
            routing_key="notification.sent", 
            body=notification_message
        )
        
        # Also publish specific notification type 
        print(f"  Publish message with routing_key=notification.{notification_type}\n")
        channel.basic_publish(
            exchange=exchange_name, 
            routing_key=f"notification.{notification_type}", 
            body=notification_message
        )
        
        return {
            "code": 201,
            "data": notification_result["data"],
            "message": "Notification sent successfully."
        }
    else:
        # Publish notification error
        print("  Publish message with routing_key=notification.error\n")
        channel.basic_publish(
            exchange=exchange_name,
            routing_key="notification.error",
            body=notification_message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        
        return {
            "code": 500,
            "data": notification_result,
            "message": "Failed to send notification."
        }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for sending notifications...")
    connectAMQP()
    app.run(host="0.0.0.0", port=5200, debug=True)