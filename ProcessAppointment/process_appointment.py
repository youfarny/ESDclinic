from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from os import environ
from datetime import datetime
from invokes import invoke_http
import requests
app = Flask(__name__)
CORS(app)

# Define service URLs
# ip_address = environ.get("IP_ADDRESS", "116.15.73.191")

ip_address = 'localhost'
appointment_URL = f"http://{ip_address}:5100/appointment"
new_appointment_URL = f"http://{ip_address}:5100/appointment/new"
patient_URL = f"http://{ip_address}:5102/patient/contact"
queue_URL = f"http://{ip_address}:5103/queue"
prescription_URL = f"http://{ip_address}:5104/prescription"
payment_URL = f"http://{ip_address}:5105/payment"

# BEFORE APPOINTMENT
@app.route("/process_new", methods=['POST'])
def process_appointment_before():
    if request.is_json:
        try:
            appointment_data = request.get_json()
            print("\nReceived an appointment request:", appointment_data)

            patient_id = appointment_data.get("patient_id")
            request_doctor = appointment_data.get("request_doctor", "").strip()
            doctor_name = appointment_data.get("doctor_name", "")
            patient_contact = appointment_data.get("patient_contact")
            patient_symptoms = appointment_data.get("patient_symptoms")

            if not patient_id:
                return jsonify({"code": 400, "message": "Missing required field: patient_id"}), 400

            if not patient_contact:
                return jsonify({"code": 400, "message": "Missing patient contact information"}), 400
            
            selected_doctor_id = None


            # If doctor_name is provided, get doctor_id
            if request_doctor:
                print(f"\nFetching doctor ID for {request_doctor}...")
                doctor_search_result = invoke_http(f"https://personal-73tajzpf.outsystemscloud.com/Doctor_service/rest/DoctorAPI/doctor/byname?doctor_name={doctor_name}", method='GET')
                print('Doctor search result:', doctor_search_result)

                if (
                    "Result" in doctor_search_result and 
                    doctor_search_result["Result"]["Success"] and 
                    "Doctor" in doctor_search_result and 
                    len(doctor_search_result["Doctor"]) > 0
                ):
                    selected_doctor_id = doctor_search_result["Doctor"][0]["doctor_id"]
                    print(f"Doctor ID for {doctor_name}: {selected_doctor_id}")
                else:
                    return jsonify({"code": 400, "message": "Invalid doctor name provided"}), 400

            # If doctor_name is empty & previous_doctor is True → Get the last doctor from past appointments
            elif request_doctor=="same":
                print("\nFetching previous doctor from past appointments...")
                previous_appointments = invoke_http(f"{appointment_URL}/records/{patient_id}", method='GET')
                print("Previous appointments:", previous_appointments)

                if isinstance(previous_appointments, list) and len(previous_appointments) > 0:
                    # Sort appointments by start_time (assuming ISO format: YYYY-MM-DDTHH:MM:SS)
                    sorted_appointments = sorted(previous_appointments, key=lambda x: x.get("start_time") or "", reverse=True)

                    last_appointment = sorted_appointments[0]  # Most recent appointment

                    # Extract doctor_id safely
                    selected_doctor_id = last_appointment.get("doctor_id")

                    if selected_doctor_id:
                        print(f"Assigned previous doctor: {selected_doctor_id}")
                    else:
                        print("Previous doctor found, but doctor_id is missing.")
                else:
                    print("No previous doctor found, fallback to shortest queue.")

            # If no doctor is assigned yet, assign based on shortest queue
            if not selected_doctor_id:
                print("\nAssigning doctor from shortest queue...")
                queue_result = invoke_http(f"{queue_URL}/shortest", method='GET')
                print("Queue result:", queue_result)

                if "error" not in queue_result and queue_result.get("doctor_id"):
                    selected_doctor_id = queue_result["doctor_id"]
                    print(f"Assigned doctor with shortest queue: {selected_doctor_id}")
                else:
                    return jsonify({"code": 500, "message": "Failed to assign doctor"}), 500
                
            # Create a new appointment
            # print("\nCreating a new appointment for the patient...")
            appointment_data = {
                "patient_id": patient_id,
                "doctor_id": selected_doctor_id,
                "patient_symptoms": patient_symptoms
            }
            new_appointment_result = invoke_http(new_appointment_URL, method='POST', json=appointment_data)
            # print("New appointment result:", new_appointment_result)

            if "error" in new_appointment_result or "appointment_id" not in new_appointment_result:
                return jsonify({"code": 500, "message": "Failed to create a new appointment", "data": new_appointment_result}), 500

            appointment_id = new_appointment_result["appointment_id"]


            # Fetch doctor details for selected doctor
            doctor_result = invoke_http(f"https://personal-73tajzpf.outsystemscloud.com/Doctor_service/rest/DoctorAPI/doctor/byid?doctor_id={selected_doctor_id}", method='GET')            
            print("Selected doctor result:", doctor_result)

            if "error" in doctor_result:
                return jsonify({"code": 500, "message": "Failed to retrieve doctor details", "data": doctor_result}), 500

            # Add appointment to queue
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
                    "appointment_result": new_appointment_result,
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


# START APPOINTMENT
@app.route("/process_appointment_start", methods=['POST'])
def process_appointment_start():
    """
    Starts an appointment for a doctor by retrieving the next patient from the queue.
    - Gets the next appointment in the queue.
    - Deletes it from the queue.
    - Fetches appointment details.
    - Updates the appointment with start_time and notes.
    - Retrieves the patient's allergies from the patient database.
    - Returns the updated appointment details along with the allergies.
    """
    try:
        data = request.get_json()
        doctor_id = data.get("doctor_id")
        notes = data.get("notes", "")  # Optional notes
        start_time = data.get("startTime", datetime.now().isoformat())

        if not doctor_id:
            return jsonify({"code": 400, "message": "Missing required field: doctor_id"}), 400

        # Get the next appointment from the queue
        print(f"Fetching next appointment for doctor_id: {doctor_id}")
        queue_response = requests.get(f"{queue_URL}/next_start/{doctor_id}")
        queue_data = queue_response.json()

        if "appointment_id" not in queue_data:
            return jsonify({"code": 404, "message": "No appointments in queue"}), 404

        appointment_id = queue_data["appointment_id"]

        # Delete appointment from queue
        print(f"Deleting appointment {appointment_id} from queue...")
        delete_response = requests.delete(f"{queue_URL}/{doctor_id}/{appointment_id}")
        delete_data = delete_response.json()

        if "error" in delete_data:
            print(f"Warning: Failed to delete appointment {appointment_id} from queue:", delete_data)

        # Get full appointment details
        print(f"Fetching details for appointment_id: {appointment_id}")
        appointment_response = requests.get(f"{appointment_URL}/{appointment_id}")

        print(f"Appointment API Response Status: {appointment_response.status_code}")
        print(f"Appointment API Response Content: {appointment_response.text}")

        if appointment_response.status_code != 200 or not appointment_response.text.strip():
            return jsonify({"code": 404, "message": "Appointment not found"}), 404

        appointment_data = appointment_response.json()

        if "error" in appointment_data:
            return jsonify({"code": 404, "message": "Appointment not found"}), 404
        
        # Get patient_id and symptoms from appointment data
        patient_id = appointment_data.get("patient_id")
        
        patient_symptoms = appointment_data.get("patient_symptoms", "Unknown symptoms")
        if not patient_id:
            return jsonify({"code": 500, "message": "Failed to retrieve patient_id from appointment"}), 500

        # Fetch patient allergies
        print(f"Fetching allergies for patient_id: {patient_id}")
        allergies_response = requests.get(f"{patient_URL}/patient/allergies/{patient_id}")
        print(f"Allergy API Response Status: {allergies_response.status_code}")
        print(f"Allergy API Response Content: {allergies_response.text}")

        if allergies_response.status_code == 200 and allergies_response.text.strip():
            allergies_data = allergies_response.json()
            patient_allergies = allergies_data.get("allergies", ["No known allergies"])
        else:
            patient_allergies = []

        # Update appointment with start_time & notes
    
        update_payload = {
            "appointment_id": appointment_id, 
            "start_time": start_time,
            "notes": notes
        }

        print(f"Updating appointment {appointment_id} with start_time and notes...")
        update_payload = {
            "appointment_id": appointment_id, 
            "startTime": start_time,  # Ensure field name matches backend
            "notes": notes
        }

        print(f"Sending PATCH request to {appointment_URL}/appointment_start with payload:")
        print(update_payload)

        update_response = requests.patch(f"{appointment_URL}/appointment_start", json=update_payload)

        print(f"Update API Response Status: {update_response.status_code}")
        print(f"Update API Response Content: {update_response.text}")

        if update_response.status_code != 200 or not update_response.text.strip():
            return jsonify({
                "code": 500, 
                "message": "Failed to update appointment", 
                "error": "Empty response from update API"
            }), 500

        update_data = update_response.json()

        if "error" in update_data:
            return jsonify({"code": 500, "message": "Failed to update appointment", "error": update_data}), 500

        # Return appointment details to the doctor
        return jsonify({
            "code": 200,
            "message": "Appointment started successfully",
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "patient_allergies": patient_allergies,
            "patient_symptoms": patient_symptoms
        }), 200
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"code": 500, "message": "Internal server error", "error": str(e)}), 500
    


@app.route("/process_appointment_end", methods=['POST'])
def process_appointment_end():
    """
    Ends an appointment by updating the appointment details with end time, diagnosis, and medicine.
    - Creates a prescription if medicine is provided.
    - Updates the appointment record with end time, diagnosis, and prescription ID.
    """
    try:
        data = request.get_json()
        appointment_id = data.get("appointment_id")
        diagnosis = data.get("diagnosis", "")
        medicine = data.get("medicine", "")
        end_time = data.get("end_time", datetime.now().isoformat())

        if not appointment_id:
            return jsonify({"code": 400, "message": "Missing required field: appointment_id"}), 400

        # 1. Fetch Appointment Details
        print(f"Fetching details for appointment_id: {appointment_id}")
        appointment_response = requests.get(f"{appointment_URL}/{appointment_id}")
        if appointment_response.status_code != 200:
            return jsonify({"code": 404, "message": "Appointment not found"}), 404

        appointment_data = appointment_response.json()
        patient_id = appointment_data.get("patient_id")

        # 2. Create Prescription if Provided
        prescription_id = None
        if medicine:
            try:
                print(f"Creating prescription for appointment_id: {appointment_id}")
                prescription_payload = {
                    "appointment_id": appointment_id,
                    "medicine": medicine
                }
                print(f"Prescription payload: {prescription_payload}")
                prescription_response = requests.post(f"{prescription_URL}", json=prescription_payload)
                
                print(f"Prescription response status: {prescription_response.status_code}")
                print(f"Prescription response content: {prescription_response.text}")
                
                # Accept both 200 and 201 as success status codes
                if prescription_response.status_code in [200, 201]:
                    prescription_data = prescription_response.json()
                    prescription_id = prescription_data.get("prescription_id")
                    print(f"Successfully created prescription with ID: {prescription_id}")
                else:
                    print(f"Warning: Failed to create prescription. Status: {prescription_response.status_code}")
                    print(f"Response content: {prescription_response.text}")
            except Exception as e:
                print(f"Exception during prescription creation: {str(e)}")
                # Continue with the appointment update even if prescription creation fails

        # 3. Update Appointment with End Time, Diagnosis and Prescription ID
        update_payload = {
            "appointment_id": appointment_id,
            "end_time": end_time,
            "diagnosis": diagnosis,
            "prescription_id": prescription_id
        }
            
        print(f"Updating appointment {appointment_id} with payload: {update_payload}")
        # Using the original endpoint that was in your code
        update_response = requests.patch(f"{appointment_URL}/appointment_end", json=update_payload)
        
        if update_response.status_code != 200:
            print(f"Failed to update appointment. Status: {update_response.status_code}")
            print(f"Response content: {update_response.text}")
            return jsonify({"code": 500, "message": f"Failed to update appointment: {update_response.text}"}), 500

        print(f"Appointment update response: {update_response.text}")
        
        return jsonify({
            "code": 200,
            "message": "Appointment ended successfully",
            "data": {
                "appointment_id": appointment_id,
                "diagnosis": diagnosis,
                "end_time": end_time,
                "prescription_id": prescription_id
            }
        }), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"code": 500, "message": "Internal server error", "error": str(e)}), 500

# AFTER APPOINTMENT
@app.route("/process_appointment_after", methods=['POST'])
def process_appointment_after():
    """
    Handles the post-appointment workflow including prescription retrieval,
    payment processing, and notifications
    """
    if request.is_json:
        try:
            # Extract data from the request
            data = request.get_json()
            print("\nReceived post-appointment request:", data)
            
            appointment_id = data.get("appointment_id")
            patient_id = data.get("patient_id")
            prescription_id = data.get("prescription_id")

            if not appointment_id:
                return jsonify({"code": 400, "message": "Missing required field: appointment_id"}), 400
            
            # 1) Request appointment info
            print(f"\nFetching appointment details for ID: {appointment_id}...")
            appointment_result = invoke_http(f"{appointment_URL}/{appointment_id}", method='GET')
            print('Appointment result:', appointment_result)
            
            if "error" in appointment_result:
                return jsonify({
                    "code": 500, 
                    "message": "Failed to retrieve appointment details", 
                    "data": appointment_result
                }), 500
            
            # Extract necessary details
            if not patient_id:
                patient_id = appointment_result.get("patient_id")
                if not patient_id:
                    return jsonify({"code": 400, "message": "Missing patient_id in appointment data"}), 400
            
            start_time = appointment_result.get("start_time")
            end_time = appointment_result.get("end_time")
            
            # 2) Process payment
            payment_data = {
                "appointment_id": appointment_id,

                "payment_amount": 50.0  # Replace with actual logic to determine the amount
            }

            print("\nPosting payment information...")
            process_payment = invoke_http(f"{payment_URL}", method='POST', json=payment_data)
            print('Process payment result:', process_payment)

            if "error" in process_payment:
                return jsonify({
                    "code": 500, 
                    "message": "Failed to process payment information", 
                    "data": process_payment
                }), 500

            payment_id = process_payment.get("payment_id")
            payment_status = process_payment.get("payment_status", False)  # Default to False if not provided
            
            # 3) Get prescription details (optional)
            prescription_result = {"message": "No prescription required"}
            if prescription_id:
                print(f"\nFetching prescription details for ID: {prescription_id}...")
                prescription_result = invoke_http(f"{prescription_URL}/{prescription_id}", method='GET')
                print('Prescription result:', prescription_result)
                
                if "error" in prescription_result:
                    print(f"Warning: Failed to retrieve prescription details: {prescription_result}")

            # 4) Check insurance information
            print(f"\nFetching patient details for ID: {patient_id}...")
            patient_result = invoke_http(f"{patient_URL}/{patient_id}", method='GET')
            print('Patient result:', patient_result)
            
            if "error" in patient_result:
                return jsonify({
                    "code": 500, 
                    "message": "Failed to retrieve patient details", 
                    "data": patient_result
                }), 500
            
            patient_contact = patient_result.get("patient_contact")
            patient_insurance = patient_result.get("insurance", {})
            
            # # 5) Send payment notification
            # notification_data = {
            #     "patient_contact": patient_contact,
            #     "payment_amount": payment_data["payment_amount"],
            #     "appointment_id": appointment_id,
            #     "payment_id": payment_id
            # }
            
            # print("\nSending payment notification...")
            # notification_result = invoke_http(f"{notification_URL}", method='POST', json=notification_data)
            # print('Notification result:', notification_result)
            
            # if "error" in notification_result:
            #     print(f"Warning: Failed to send notification: {notification_result}")


            
            # 6) Check payment status
            print("\nChecking payment status...")
            check_result = invoke_http(f"{payment_URL}/{payment_id}", method='GET')
            print('Check result:', check_result)

            if "error" in check_result:
                return jsonify({
                    "code": 500,
                    "message": "Failed to verify payment status",
                    "data": check_result
                }), 500
            
            return jsonify({
                "code": 200,
                "message": "Post-appointment processing completed successfully",
                "data": {
                    "appointment_details": appointment_result,
                    "prescription_details": prescription_result,
                    "payment_details": {
                        "payment_id": payment_id,
                        "payment_status": check_result.get("success", False),
                        "payment_amount": payment_data["payment_amount"]
                    },
                    "insurance_details": patient_insurance,
                
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



if __name__ == "__main__":
    print("Starting process_appointment microservice...")
    app.run(host="0.0.0.0", port=5000, debug=True)


