from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

appointment_URL = "http://localhost:5000/appointment"
doctor_URL = "http://localhost:5001/doctor"
patient_URL = "http://localhost:5002/patient"
notification_URL = "http://localhost:5003/notification"
prescription_URL = "http://localhost:5004/prescription"
payment_URL = "http://localhost:5005/payment"
error_URL = "http://localhost:5006/error"

@app.route("/process_appointment", methods=['POST'])
def process_appointment():
    if request.is_json:
        try:
            appointment_data = request.get_json()
            print("\nReceived an appointment request in JSON:", appointment_data)

            result = handle_appointment(appointment_data)
            return jsonify(result), result["code"]

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "process_appointment.py internal error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processAppointment(appointment_data):
      # 1. Send appointment info to appointment microservice
    print('\n-----Invoking appointment microservice-----')
    appointment_result = invoke_http(appointment_URL, method='POST', json=appointment_data)
    print('appointment_result:', appointment_result)

    # Record the activity log
    print('\n\n-----Invoking activity_log microservice-----')
    invoke_http(activity_log_URL, method="POST", json=appointment_result)
    print("\nAppointment request sent to activity log.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails

    # Check the appointment result; if a failure, send it to the error microservice.
    code = appointment_result["code"]
    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Invoking error microservice as appointment creation fails-----')
        invoke_http(error_URL, method="POST", json=appointment_result)
        print("Appointment status ({:d}) sent to the error microservice:".format(
            code), appointment_result)

        # Return error
        return {
            "code": 500,
            "data": {"appointment_result": appointment_result},
            "message": "Appointment creation failure sent for error handling."
        }
    
    # 2. Get doctor availability if needed
    if "doctor_id" in appointment_data:
        print('\n\n-----Invoking doctor microservice to check availability-----')
        doctor_result = invoke_http(
            doctor_URL + "/" + str(appointment_data["doctor_id"]), method="GET")
        print("doctor_result:", doctor_result, '\n')
        
        # Check if doctor is available
        if "available" in doctor_result["data"] and not doctor_result["data"]["available"]:
            # Inform the error microservice
            print('\n\n-----Invoking error microservice as doctor is unavailable-----')
            error_data = {
                "code": 400,
                "data": doctor_result["data"],
                "message": "Doctor is not available for this appointment."
            }
            invoke_http(error_URL, method="POST", json=error_data)
            print("Doctor unavailability sent to error microservice:", error_data)
            
            # Return error
            return {
                "code": 400,
                "data": {
                    "appointment_result": appointment_result,
                    "doctor_result": doctor_result
                },
                "message": "Doctor is not available for this appointment."
            }
    
    # 3. Process payment for appointment
    print('\n\n-----Invoking payment microservice-----')
    payment_data = {
        "appointment_id": appointment_result["data"]["appointment_id"],
        "patient_id": appointment_data["patient_id"],
        "amount": appointment_data.get("amount", 100)  # Default amount if not specified
    }
    payment_result = invoke_http(payment_URL, method="POST", json=payment_data)
    print("payment_result:", payment_result, '\n')
    
    # Check the payment result; if a failure, send it to the error microservice.
    code = payment_result["code"]
    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Invoking error microservice as payment fails-----')
        invoke_http(error_URL, method="POST", json=payment_result)
        print("Payment status ({:d}) sent to the error microservice:".format(
            code), payment_result)
        
        # Return error
        return {
            "code": 400,
            "data": {
                "appointment_result": appointment_result,
                "payment_result": payment_result
            },
            "message": "Payment processing error sent for error handling."
        }
    
    # 4. Check if patient has an existing prescription
    if "patient_id" in appointment_data:
        print('\n\n-----Invoking prescription microservice to check existing prescriptions-----')
        prescription_result = invoke_http(
            prescription_URL + "/patient/" + str(appointment_data["patient_id"]), method="GET")
        print("prescription_result:", prescription_result, '\n')
    else:
        prescription_result = {"code": 200, "data": {"prescriptions": []}}
    
    # 5. Send notification to patient
    print('\n\n-----Invoking notification microservice-----')
    notification_data = {
        "patient_id": appointment_data["patient_id"],
        "patient_contact": appointment_data.get("patient_contact", ""),
        "message": "Your appointment has been successfully booked and confirmed. " +
                  "Appointment ID: " + str(appointment_result["data"]["appointment_id"])
    }
    notification_result = invoke_http(notification_URL, method="POST", json=notification_data)
    print("notification_result:", notification_result, '\n')
    
    # Return success with all results
    return {
        "code": 201,
        "data": {
            "appointment_result": appointment_result,
            "payment_result": payment_result,
            "prescription_result": prescription_result,
            "notification_result": notification_result
        },
        "message": "Appointment processed successfully."
    }



if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for processing an appointment...")
    app.run(host="0.0.0.0", port=5200, debug=True)
