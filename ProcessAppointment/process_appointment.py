from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from os import environ
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# Define service URLs
# ip_address = environ.get("IP_ADDRESS", "116.15.73.191")

ip_address = 'localhost'
appointment_URL = f"http://{ip_address}:5100/appointment"
doctor_URL = f"http://{ip_address}:5101/doctor"
patient_URL = f"http://{ip_address}:5102/patient/contact"
queue_URL = f"http://{ip_address}:5103/queue"
prescription_URL = f"http://{ip_address}:5104/prescription"
payment_URL = f"http://{ip_address}:5105/payment"
@app.route("/process_appointment_before", methods=['POST'])
def process_appointment_before():
    if request.is_json:
        try:
            appointment_data = request.get_json()
            print("\nReceived an appointment request:", appointment_data)

            appointment_id = appointment_data.get("appointment_id")
            if not appointment_id:
                return jsonify({"code": 400, "message": "Missing required field: appointment_id"}), 400

            print("\nFetching existing appointment details...")
            appointment_result = invoke_http(f"{appointment_URL}/{appointment_id}", method='GET')
            print('Appointment result:', appointment_result)

            if "error" in appointment_result:
                return jsonify({"code": 500, "message": "Failed to retrieve the appointment", "data": appointment_result}), 500

            patient_id = appointment_result.get("patient_id")
            if not patient_id:
                return jsonify({"code": 400, "message": "Missing patient_id in appointment data"}), 400

            print("\nFetching patient details...")
            patient_result = invoke_http(f"{patient_URL}/{patient_id}", method='GET')
            print('Patient result:', patient_result)

            if "error" in patient_result:
                return jsonify({"code": 500, "message": "Failed to retrieve patient details", "data": patient_result}), 500

            patient_contact = patient_result.get("patient_contact")
            if not patient_contact:
                return jsonify({"code": 400, "message": "Missing patient contact information"}), 400

            # Determine doctor selection logic
            requested_doctor_id = appointment_result.get("doctor_id")
            selected_doctor_id = None

            if requested_doctor_id:
                # Case 1: Doctor is specifically requested
                print("\nDoctor requested by patient. Fetching doctor details...")
                doctor_result = invoke_http(f"{doctor_URL}/{requested_doctor_id}", method='GET')
                print('Doctor result:', doctor_result)

                if "error" not in doctor_result:
                    selected_doctor_id = requested_doctor_id
                else:
                    print("Requested doctor not found, falling back to previous doctor check.")

            if not selected_doctor_id:
                # Case 2: No doctor requested, check last appointment
                print("\nNo doctor requested. Checking previous appointment history...")
                previous_appointments = invoke_http(f"{appointment_URL}/patient/{patient_id}", method='GET')
                print("Previous appointments:", previous_appointments)

                if "error" not in previous_appointments and previous_appointments.get("data"):
                    last_appointment = previous_appointments["data"][-1]  # Get the most recent appointment
                    selected_doctor_id = last_appointment.get("doctor_id")
                    print(f"Previous doctor found: {selected_doctor_id}")

            if not selected_doctor_id:
                # Case 3: No previous doctor found, get the doctor with the shortest queue
                print("\nNo previous doctor found. Assigning doctor from shortest queue...")
                queue_result = invoke_http(f"{queue_URL}/shortest", method='GET')
                print("Queue result:", queue_result)

                if "error" not in queue_result and queue_result.get("doctor_id"):
                    selected_doctor_id = queue_result["doctor_id"]
                    print(f"Assigned doctor with shortest queue: {selected_doctor_id}")
                else:
                    return jsonify({"code": 500, "message": "Failed to assign doctor"}), 500

            # Fetch doctor details
            doctor_result = invoke_http(f"{doctor_URL}/{selected_doctor_id}", method='GET')
            print("Selected doctor result:", doctor_result)

            if "error" in doctor_result:
                return jsonify({"code": 500, "message": "Failed to retrieve doctor details", "data": doctor_result}), 500

            # Add to queue
            print("\nAdding appointment to queue...")
            queue_data = {
                "doctor_id": selected_doctor_id,
                "appointment_id": appointment_id,
                "patient_contact": patient_contact
            }
            queue_result = invoke_http(queue_URL, method='POST', json=queue_data)
            print('Queue result:', queue_result)

            if "error" in queue_result:
                return jsonify({"code": 500, "message": "Failed to add appointment to queue", "data": queue_result}), 500

            return jsonify({
                "code": 200,
                "message": "Appointment successfully added to queue",
                "data": {
                    "appointment_result": appointment_result,
                    "doctor_result": doctor_result,
                    "queue_result": queue_result
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

    return jsonify({"code": 400, "message": "Invalid JSON input"}), 400


@app.route("/process_appointment_during", methods=['POST'])
def process_appointment_during():
    if request.is_json:
        try:
            appointment_data = request.get_json()
            print("\nProcessing appointment during:", appointment_data)

            appointment_id = appointment_data.get("appointment_id")
            patient_id = appointment_data.get("patient_id")
            if not appointment_id or not patient_id:
                return jsonify({"code": 400, "message": "Missing required fields: appointment_id or patient_id"}), 400

            # Check for existing prescriptions
            print("\nChecking for existing prescriptions...")
            prescription_result = invoke_http(f"{prescription_URL}/patient/{patient_id}", method='GET')
            print('Prescription result:', prescription_result)

            # Process payment
            print("\n💳 Processing payment for appointment...")
            payment_data = {
                "appointment_id": appointment_id,
                "patient_id": patient_id,
                "payment_amount": appointment_data.get("amount", 100)  # Default amount if not provided
            }
            payment_result = invoke_http(payment_URL, method='POST', json=payment_data)
            print('Payment result:', payment_result)

            if "error" in payment_result:
                return jsonify({"code": 500, "message": "Payment processing failed", "data": payment_result}), 500

            return jsonify({
                "code": 200,
                "message": "Appointment processed successfully during consultation",
                "data": {
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

    return jsonify({"code": 400, "message": "Invalid JSON input"}), 400


@app.route("/process_appointment_after", methods=['POST'])
def process_appointment_after():
    if request.is_json:
        try:
            appointment_data = request.get_json()
            appointment_id = appointment_data.get("appointment_id")
            doctor_id = appointment_data.get("doctor_id")

            if not appointment_id or not doctor_id:
                return jsonify({"code": 400, "message": "Missing required fields: appointment_id or doctor_id"}), 400

            print(f"\nRemoving appointment {appointment_id} from queue...")
            delete_result = invoke_http(f"{queue_URL}/{doctor_id}/{appointment_id}", method='DELETE')
            print("Queue delete result:", delete_result)

            if "error" in delete_result:
                return jsonify({"code": 500, "message": "Failed to remove appointment from queue", "data": delete_result}), 500

            return jsonify({
                "code": 200,
                "message": "Appointment successfully removed from queue",
                "data": delete_result
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

    return jsonify({"code": 400, "message": "Invalid JSON input"}), 400
if __name__ == "__main__":
    print("Starting process_appointment microservice...")
    app.run(host="0.0.0.0", port=5000, debug=True)


