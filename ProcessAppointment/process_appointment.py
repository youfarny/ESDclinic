from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from os import environ
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# Get the IP address from an environment variable, defaulting to "116.15.73.191" if not set
# ip_address = environ.get("IP_ADDRESS", "116.15.73.191")
ip_address = 'localhost'

# Define URLs using the IP address from the environment variable
# appointment_URL = f"http://{ip_address}:5100/appointment/new"
appointment_URL = f"http://{ip_address}:5100/appointment"
doctor_URL = f"http://{ip_address}:5101/doctor"
patient_URL = f"http://{ip_address}:5102/patient/contact"
queue_URL = f"http://{ip_address}:5103/queue"
prescription_URL = f"http://{ip_address}:5104/prescription"
payment_URL = f"http://{ip_address}:5105/payment"

@app.route("/process_appointment", methods=['POST'])
def process_appointment():
    if request.is_json:
        try:
            appointment_data = request.get_json()
            print("\nReceived an appointment request in JSON:", appointment_data)

            # Ensure appointment_id exists
            appointment_id = appointment_data.get("appointment_id")
            if not appointment_id:
                return jsonify({
                    "code": 400,
                    "message": "Missing required field: appointment_id"
                }), 400

            # Step 1: Retrieve the existing appointment
            print("\nFetching existing appointment details...")
            appointment_result = invoke_http(f"{appointment_URL}/{appointment_id}", method='GET')
            print('appointment_result:', appointment_result)

            if "error" in appointment_result:
                return jsonify({
                    "code": 500,
                    "message": "Failed to retrieve the appointment",
                    "data": appointment_result
                }), 500

            patient_id = appointment_result.get("patient_id")
            if not patient_id:
                return jsonify({
                    "code": 400,
                    "message": "Missing patient_id in appointment data"
                }), 400

            print("\nFetching patient details...")
            patient_result = invoke_http(f"{patient_URL}/{patient_id}", method='GET')
            print('patient_result:', patient_result)

            # Check if the patient service returned invalid JSON
            if "Invalid JSON output from service" in str(patient_result.get("message", "")):
                return jsonify({
                    "code": 503,
                    "message": "Patient service is not responding correctly",
                    "data": {"patient_result": patient_result}
                }), 503

            if "error" in patient_result:
                return jsonify({
                    "code": 500,
                    "message": "Failed to retrieve patient details",
                    "data": patient_result
                }), 500

            # Extract patient_contact with more detailed error handling
            print(f"Full patient result: {patient_result}")  # Debug the entire patient result
            patient_contact = patient_result.get("patient_contact")
            print(f"patient_contact value: {patient_contact}")  # Debug the contact value

            if patient_contact is None:
                return jsonify({
                    "code": 400,
                    "message": "Patient contact information is missing but required for queue",
                    "data": {"patient_result": patient_result}  # Include the patient data in the error
                }), 400
            

            # Step 2: Get doctor information if a specific doctor is requested
            doctor_id = appointment_result.get("doctor_id")
            doctor_result = None
            if doctor_id:
                print("\n🩺 Fetching doctor details...")
                doctor_result = invoke_http(f"{doctor_URL}/{doctor_id}", method='GET')
                print('doctor_result:', doctor_result)

                if "error" in doctor_result:
                    return jsonify({
                        "code": 500,
                        "message": "Failed to retrieve doctor details",
                        "data": doctor_result
                    }), 500

            # Step 3: Add the appointment to the queue
            patient_id = appointment_result.get("patient_id")
            if not patient_id:
                return jsonify({
                    "code": 400,
                    "message": "Missing patient_id in appointment data"
                }), 400

            # Get patient information to retrieve patient_contact
            print("\n Fetching patient details...")
            patient_result = invoke_http(f"{patient_URL}/{patient_id}", method='GET')
            print('patient_result:', patient_result)

            if "error" in patient_result:
                return jsonify({
                    "code": 500,
                    "message": "Failed to retrieve patient details",
                    "data": patient_result
                }), 500

            # Extract patient_contact and validate it's not null
            patient_contact = patient_result.get("patient_contact")
            if patient_contact is None:
                return jsonify({
                    "code": 400,
                    "message": "Patient contact information is missing but required for queue"
                }), 400
            print("\nAdding appointment to the queue...")
            queue_data = {
                "doctor_id": doctor_id,
                "appointment_id": appointment_id,
                "patient_contact": patient_contact,
            }
            queue_result = invoke_http(queue_URL, method='POST', json=queue_data)
            print('queue_result:', queue_result)

            if "error" in queue_result:
                return jsonify({
                    "code": 500,
                    "message": "Failed to add appointment to queue",
                    "data": queue_result
                }), 500

            # Step 4: Check for existing prescriptions
            patient_id = appointment_result.get("patient_id")
            prescription_result = {"code": 200, "data": {"prescriptions": []}}
            if patient_id:
                print("\nChecking for existing prescriptions...")
                prescription_result = invoke_http(f"{prescription_URL}/patient/{patient_id}", method='GET')
                print('prescription_result:', prescription_result)

            # Step 5: Process payment for appointment
            print("\n💳 Processing payment for appointment...")
            payment_data = {
                "appointment_id": appointment_id,
                "patient_id": patient_id,
                "amount": appointment_data.get("amount", 100)  # Default amount if not specified
            }
            payment_result = invoke_http(payment_URL, method='POST', json=payment_data)
            print('payment_result:', payment_result)

            if "error" in payment_result:
                return jsonify({
                    "code": 500,
                    "message": "Payment processing failed",
                    "data": payment_result
                }), 500

            # Return success response
            return jsonify({
                "code": 200,
                "message": "Appointment processed successfully",
                "data": {
                    "appointment_result": appointment_result,
                    "doctor_result": doctor_result,
                    "queue_result": queue_result,
                    "prescription_result": prescription_result,
                    "payment_result": payment_result
                }
            }), 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = f"{str(e)} at {str(exc_type)}: {fname}: line {str(exc_tb.tb_lineno)}"
            print("ERROR:", ex_str)

            return jsonify({
                "code": 500,
                "message": "Internal server error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input"
    }), 400


if __name__ == "__main__":
    print("Starting process_appointment microservice...")
    app.run(host="0.0.0.0", port=5000, debug=True)