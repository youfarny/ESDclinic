from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import uuid
from os import environ
from datetime import datetime, timedelta, timezone
from invokes import invoke_http
import requests
from google import genai
# import google.generativeai as genai
import json
import pika
app = Flask(__name__)
CORS(app)

# Define service URLs


# ip_address = 'localhost'
ip_address = environ.get("IP_ADDRESS", "116.15.73.191")

appointment_URL = f"http://{ip_address}:5100/appointment"
patient_URL = f"http://{ip_address}:5102/patient"
queue_URL = f"http://{ip_address}:5103/queue"
prescription_URL = f"http://{ip_address}:5104/prescription"
payment_URL = f"http://{ip_address}:5105/payment"
notification_URL = f"http://{ip_address}:5672/send_notification"

# BEFORE APPOINTMENT
@app.route("/process/new", methods=['POST'])
def process_appointment_new():
    """
    {
        "apikey": "admin",
        "patient_id": 1,
        "request_doctor": "",
        "patient_symptoms": ["Fever", "Headache"],
        "patient_contact": 91234567
    }
    """


    # 3 Get recommended doctor using 
    # patient_id, request_doctor, patient_symptoms, patient_contact

    print("\n\n")
    print("------------------------------STEP 3------------------------------")
    if request.is_json:
        try:
            appointment_data = request.get_json()
            print("\nReceived an appointment request:", appointment_data)

            patient_id = appointment_data.get("patient_id")
            request_doctor = appointment_data.get("request_doctor", "").strip()
            patient_contact = appointment_data.get("patient_contact")
            patient_symptoms = appointment_data.get("patient_symptoms")

            if not patient_id:
                return jsonify({"code": 400, "message": "Missing required field: patient_id"}), 400

            if not patient_contact:
                return jsonify({"code": 400, "message": "Missing patient contact information"}), 400
            






            if request_doctor=='' or request_doctor=='same':

                # A1 If no doctor is requested, get shortest queue doctor
                # A2 Return doctor
                if request_doctor=='':
                    print("\n\n")
                    print("------------------------------STEP A1 & A2------------------------------")
                    print("\nAssigning doctor from shortest queue...")
                    queue_result = invoke_http(f"{queue_URL}/shortest", method='GET')
                    

                    if "error" not in queue_result and queue_result.get("doctor_id"):
                        selected_doctor_id = queue_result["doctor_id"]
                        print(f"Assigned doctor_id with shortest queue: {selected_doctor_id}")
                    else:
                        return jsonify({"code": 500, "message": "Failed to assign doctor"}), 500
                    
                # B1 Get patient records
                # B2 Return patient's records → Get the previous doctor 
                elif request_doctor=="same":
                    print("\n\n")
                    print("------------------------------STEP B1 & B2------------------------------")
                    print("\nFetching previous doctor from past appointments...")
                    previous_appointments = invoke_http(f"{appointment_URL}/records/{patient_id}", method='GET')

                    if isinstance(previous_appointments, list) and len(previous_appointments) > 0:

                        # Sort appointments by start_time (assuming ISO format: YYYY-MM-DDTHH:MM:SS)
                        sorted_appointments = sorted(previous_appointments, key=lambda x: x.get("start_time") or "", reverse=True)
                        # Most recent appointment
                        last_appointment = sorted_appointments[0]  
                        print("Most recent appointment:", last_appointment)
                        # Extract doctor_id safely
                        selected_doctor_id = last_appointment.get("doctor_id")

                        if selected_doctor_id:
                            print(f"Assigned previous doctor: {selected_doctor_id}")
                        else:
                            print("Previous doctor found, but doctor_id is missing.")
                    else:
                        print("No previous doctor found, fallback to shortest queue.")


                # A3 B3 Request doctor_name using doctor_id
                # A4 B4 Return doctor_name
                doctor_info = invoke_http(f"https://personal-73tajzpf.outsystemscloud.com/Doctor_service/rest/DoctorAPI/doctor/byid?doctor_id={selected_doctor_id}", method='GET')
                doctor_name = doctor_info["Doctor"][0]["doctor_name"]
                print(f"Assigned Doctor Name: {doctor_name}")


            
            else:
                # C1 Get doctor_id if doctor is requested
                # C2 Return doctor_id
                print("\n\n")
                print("------------------------------STEP C1 & C2------------------------------")
                doctor_name = request_doctor
                print(f"\nFetching doctor ID for {request_doctor}...")
                doctor_search_result = invoke_http(f"https://personal-73tajzpf.outsystemscloud.com/Doctor_service/rest/DoctorAPI/doctor/byname?doctor_name={request_doctor}", method='GET')
                print(f"Assigned Doctor Name: {doctor_name}")

                if (
                    "Result" in doctor_search_result and 
                    doctor_search_result["Result"]["Success"] and 
                    "Doctor" in doctor_search_result and 
                    len(doctor_search_result["Doctor"]) > 0
                ):
                    selected_doctor_id = doctor_search_result["Doctor"][0]["doctor_id"]
                    print(f"Doctor ID for {request_doctor}: {selected_doctor_id}")
                else:
                    return jsonify({"code": 400, "message": "Invalid doctor name provided"}), 400

        






        
            # 5 Create a new appointment {patient_id, doctor_id, symptoms}
            # 6 Return new appointment {appointment_id}
           
            appointment_data = {
                "patient_id": patient_id,
                "doctor_id": selected_doctor_id,
                "patient_symptoms": patient_symptoms
            }
            print("\n\n")
            print("------------------------------STEP 5 & 6------------------------------")
            print(f"Creating new appointment")
            new_appointment_result = invoke_http(f"{appointment_URL}/new", method='POST', json=appointment_data)

            if "error" in new_appointment_result or "appointment_id" not in new_appointment_result:
                return jsonify({"code": 500, "message": "Failed to create a new appointment", "data": new_appointment_result}), 500

            new_appointment_id = new_appointment_result["appointment_id"]
            print("New apppointment ID: ", new_appointment_id)


            # 7 {doctor_id, doctor_name, appointment_id, patient_contact}
            print("\n\n")
            print("------------------------------STEP 7------------------------------")

            
            # Prepare the payload with required data
            notification_data = {
                "notification_type": "appointment_confirmation",
                "appointment_id": new_appointment_id, 
                "doctor_id": selected_doctor_id,   
                "doctor_name": doctor_name,     
                "patient_contact": patient_contact,
                "appointment_type": "before" 
            }
            # AMQP connection parameters
            queue_name = "sms_queue"
            response_queue = None
            queue_length = None
            correlation_id = str(uuid.uuid4())
         

            print(notification_data)

            credentials = pika.PlainCredentials('admin', 'ESD213password!')
            parameters = pika.ConnectionParameters(host=ip_address, credentials=credentials)
            
            # Establish connection and channel
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            channel.exchange_declare(exchange='esd_clinic', exchange_type='topic', durable=True)
            # Ensure the queue exists (durable = True for persistence)
            result =channel.queue_declare(queue=queue_name)
            callback_queue = result.method.queue
            def on_response(ch, method, props, body):
                nonlocal queue_length
                if props.correlation_id == correlation_id:
                    response = json.loads(body)
                    queue_length = response.get('queue_length')

            channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)

            # Publish the message with persistence and content-type
            channel.basic_publish(
                exchange='esd_clinic',
                routing_key="notification",
                body=json.dumps(notification_data),
                properties=pika.BasicProperties(
                    reply_to=callback_queue,
                    correlation_id=correlation_id,
                    delivery_mode=2,  # Make message persistent
                    content_type='application/json'
                )
            )

            # print(f"Notification for appointment {new_appointment_id} sent to '{queue_name}'.")

            print(f"Waiting for queue_length response for appointment {new_appointment_id}...")

            # Wait for the response
            while queue_length is None:
                connection.process_data_events(time_limit=1)

            print(f"Queue length for appointment {new_appointment_id}: {queue_length}")

            connection.close()

            """
            # Send the POST request
            response = requests.post(notification_URL, json=notification_data)

            # Process the response
            queue_length = None
            if response.status_code in range(200, 300):
                result = response.json()
                queue_length = result.get("data", {}).get("queue_length")
                print(f"Queue length for appointment {new_appointment_id}: {queue_length}")
            else:
                print(f"Error in notification service: {response.status_code} - {response.text}")
            """




            # 11 Return new appointment {appointment_id, doctor_name, doctor_id, queue_length}
            return jsonify({
                "code": 200,
                "message": "Appointment created successfully",
                "data": {
                    "appointment_id": new_appointment_id,
                    "doctor_name": doctor_name,
                    "doctor_id": selected_doctor_id,
                    "queue_length": queue_length
                }
            }), 200

        except Exception as e:
            print("ERROR:", str(e))
            return jsonify({"code": 500, "message": "Internal server error", "error": str(e)}), 500

    return jsonify({"code": 400, "message": "Invalid JSON input"}), 400


# START APPOINTMENT
@app.route("/process/start", methods=['POST'])
def process_appointment_start():
    """
    Starts an appointment for a doctor by retrieving the next patient from the queue.
    - Gets the next appointment in the queue.
    - Deletes it from the queue.
    - Fetches appointment details.
    - Updates the appointment with start_time and notes.
    - Retrieves the patient's allergies from the patient database.
    - Returns the updated appointment details along with the allergies.
    - {doctor_id: 1}
    """
    print("\n\n")
    print("!!!------------------------------NEW REQUEST TO /process/start------------------------------!!!")
    gmt_plus_8 = timezone(timedelta(hours=8))
    start_time = datetime.now(gmt_plus_8).isoformat()
    print(start_time)


    # 1 Get next appointment  {doctor_id}
    print("\n\n")
    print("------------------------------STEP 1------------------------------")
    try:
        data = request.get_json()
        print(data)
        doctor_id = data.get("doctor_id")

        if not doctor_id:
            return jsonify({"code": 400, "message": "Missing required field: doctor_id"}), 400
        




        # 2 Get the next appointment from the queue {doctor_id}
        # 3 Return next appointment {doctor_id, appointment_id}
        print("\n\n")
        print("------------------------------STEP 2 & 3------------------------------")
        print(f"Fetching next appointment for doctor_id: {doctor_id}")
        queue_response = requests.get(f"{queue_URL}/next/{doctor_id}")
        queue_data = queue_response.json()

        if "appointment_id" not in queue_data:
            return jsonify({"code": 404, "message": "No appointments in queue"}), 404

        appointment_id = queue_data["appointment_id"]






        # 4 Delete appointment from queue {appointment_id}
        print("\n\n")
        print("------------------------------STEP 4------------------------------")
        print(f"Deleting appointment {appointment_id} from queue...")
        delete_response = requests.delete(f"{queue_URL}/{doctor_id}/{appointment_id}")
        delete_data = delete_response.json()

        if "error" in delete_data:
            print(f"Warning: Failed to delete appointment {appointment_id} from queue:", delete_data)







        # 5 Get full appointment details {appointment_id}
        # 6 Return appointment details {...}
        print("\n\n")
        print("------------------------------STEP 5 & 6------------------------------")
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


        



        # 7 Patient allergies {patient_id}
        # 8 Return patient allergies {patient_id, patient_allergies}
        print("\n\n")
        print("------------------------------STEP 7 & 8------------------------------")
        print(f"Fetching allergies for patient_id: {patient_id}")
        print(f"{patient_URL}/patient/allergies/{patient_id}")
        allergies_response = requests.get(f"{patient_URL}/allergies/{patient_id}")
        print(f"Allergy API Response Status: {allergies_response.status_code}")
        print(f"Allergy API Response Content: {allergies_response.text}")

        if allergies_response.status_code == 200 and allergies_response.text.strip():
            allergies_data = allergies_response.json()
            patient_allergies = allergies_data.get("allergies", ["No known allergies"])
        else:
            patient_allergies = []






        # 9 Send symptoms to AI {patient_symptoms}
        # 10 Return recommendations {diagnoses}
        print("\n\n")
        print("------------------------------STEP 9 & 10------------------------------")
        patient_symptoms = appointment_data.get("patient_symptoms", "Unknown symptoms")

        if not patient_id:
            return jsonify({"code": 500, "message": "Failed to retrieve patient_id from appointment"}), 500

        client = genai.Client(api_key="AIzaSyAWkKyubwXAJYDMdf40qNkwWwaEkY-MVTA")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"You are a diagnosis recommender for a project. You will receive a list of symptoms and return 5 possible diagnoses with your confidence level from 0 to 100% in descending order. Return your results in json format and nothing else. There are the symptoms: {patient_symptoms} "
        )

        # print(response.text)
        clean_output = response.text.replace('```json', '').replace('```', '').strip()

        recommended_diagnoses = json.loads(clean_output)

        print(recommended_diagnoses)     







        # Zoom?








        # 11 Update appointment {appointment_id, notes}
        print("\n\n")
        print("------------------------------STEP 11------------------------------")
        
        update_payload = {
            "appointment_id": appointment_id, 
            "startTime": start_time,  # Ensure field name matches backend
            "notes": recommended_diagnoses
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
        







        # 12 Return appointment details to the doctor
        print("\n\n")
        print("------------------------------STEP 12------------------------------")
        return jsonify({
            "code": 200,
            "message": "Appointment started successfully",
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "patient_allergies": patient_allergies,
            "patient_symptoms": patient_symptoms,
            "notes": recommended_diagnoses
        }), 200
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"code": 500, "message": "Internal server error", "error": str(e)}), 500
    


@app.route("/process/end", methods=['POST'])
def process_appointment_end():
    """
    Ends an appointment by updating the appointment details with end time, diagnosis, and medicine.
    - Creates a prescription if medicine is provided.
    - Updates the appointment record with end time, diagnosis, and prescription ID.
    - {
        appointment_id: 1,
        patient_id: 1,
        diagnosis: "Flu",
        medicine: ["Antibiotics", "Antihistamines"]
      }
    """

    print("\n\n")
    print("!!!------------------------------NEW REQUEST TO /process/end------------------------------!!!")
    gmt_plus_8 = timezone(timedelta(hours=8))
    end_time = datetime.now(gmt_plus_8).isoformat()
    print(end_time)

    # 13 Send appointment info at end of appointment
    print("\n\n")
    print("------------------------------STEP 13------------------------------")
    try:
        data = request.get_json()
        appointment_id = data.get("appointment_id")
        patient_id = data.get("patient_id")
        diagnosis = data.get("diagnosis", "")
        medicine = data.get("medicine", "")

        if not appointment_id:
            return jsonify({"code": 400, "message": "Missing required field: appointment_id"}), 400
        
        print(data)




        # 14 Send Notification to next patient in queue
        # {doctor_id} 
        print("\n\n")
        print("------------------------------STEP 14------------------------------")












        # 18 Get patient allergies {patient_id}
        # 19 Return patient allergies {patient_id, allergies} 
        # Verification for allergies
        print("\n\n")
        print("------------------------------STEP 18 & 19------------------------------")

        print(f"Fetching allergies for patient_id: {patient_id}")
        print(f"{patient_URL}/patient/allergies/{patient_id}")
        allergies_response = requests.get(f"{patient_URL}/allergies/{patient_id}")
        print(f"Allergy API Response Status: {allergies_response.status_code}")
        print(f"Allergy API Response Content: {allergies_response.text}")

        if allergies_response.status_code == 200 and allergies_response.text.strip():
            allergies_data = allergies_response.json()
            patient_allergies = allergies_data.get("allergies", ["No known allergies"])
        else:
            patient_allergies = []

        for allergy in patient_allergies:
            for medicine_i in medicine:
                if (allergy == medicine_i):
                    print("Patient is allergic to medication")
                    raise Exception("Patient is allergic to medication")











        # 20 Create new prescription {medicine}
        # 21 Return prescription_id {prescription_id} 
        print("\n\n")
        print("------------------------------STEP 20 & 21------------------------------")

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
                raise Exception(f"Exception during prescription creation: {str(e)}")










        # 22 Update diagnosis / prescription in appointment {appointment_id, end_time, diagnosis, prescription_id}
        # 23 Return success / failure {appointment_id, success} 
        print("\n\n")
        print("------------------------------STEP 22 & 23------------------------------")

        update_payload = {
            "appointment_id": appointment_id,
            "end_time": end_time,
            "diagnosis": diagnosis,
            "prescription_id": prescription_id
        }
        try:    
            print(f"Updating appointment {appointment_id} with payload: {update_payload}")
            # Using the original endpoint that was in your code
            update_response = requests.patch(f"{appointment_URL}/appointment_end", json=update_payload)
            
            if update_response.status_code != 200:
                print(f"Failed to update appointment. Status: {update_response.status_code}")
                print(f"Response content: {update_response.text}")
                return jsonify({"code": 500, "message": f"Failed to update appointment: {update_response.text}"}), 500

            print(f"Appointment update response: {update_response.text}")
        except Exception as e:
            print(f"Exception during appointment patch: {str(e)}")
            raise Exception(f"Exception during appointment patch: {str(e)}")
    












        # 24 Return success / failure {appointment_id, prescription_id, success} 
        print("\n\n")
        print("------------------------------STEP 24------------------------------")

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







        # 1. Fetch Appointment Details
        # print("\n\n")
        # print("------------------------------STEP 13------------------------------")        
        # print(f"Fetching details for appointment_id: {appointment_id}")
        # appointment_response = requests.get(f"{appointment_URL}/{appointment_id}")
        # if appointment_response.status_code != 200:
        #     return jsonify({"code": 404, "message": "Appointment not found"}), 404

        # appointment_data = appointment_response.json()
        # patient_id = appointment_data.get("patient_id")

        # 2. Create Prescription if Provided

        # 3. Update Appointment with End Time, Diagnosis and Prescription ID
        

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"code": 500, "message": "Internal server error", "error": str(e)}), 500




# AFTER APPOINTMENT
@app.route("/process/calculate", methods=['POST'])
def process_appointment_calculate():

    if request.is_json:
        try:
            # Extract data from the request
            data = request.get_json()
            print("\nReceived post-appointment request:", data)
            
            appointment_id = data.get("appointment_id")
        
            if not appointment_id:
                return jsonify({"code": 400, "message": "Missing required field: appointment_id"}), 400
            
            # 4 Get appointment info 
            # 5 Return appointment info {patient_id, start_time, end_time, prescription_id}
            print("\n\n")
            print("------------------------------STEP 4 & 5------------------------------")
            print(f"\nFetching appointment details for ID: {appointment_id}...")
            appointment_result = invoke_http(f"{appointment_URL}/{appointment_id}", method='GET')
           
            if "error" in appointment_result:
                return jsonify({
                    "code": 500, 
                    "message": "Failed to retrieve appointment details", 
                    "data": appointment_result
                }), 500
            
            # Extract necessary details
            patient_id = appointment_result.get("patient_id")
            start_time = appointment_result.get("start_time")
            end_time = appointment_result.get("end_time")
            prescription_id = appointment_result.get("prescription_id")
            print('patient_id:', patient_id)
            print('start_time:', start_time)
            print('end_time:', end_time)
            print('prescription_id:', prescription_id)
            # Convert strings to datetime objects
            start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
            end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")

            # Calculate the time difference
            time_diff = end_time - start_time
            consultation_duration_minutes = time_diff.total_seconds()/60
            consultation_duration_minutes = time_diff.total_seconds()/60
            print('Consultation duration (minute):', consultation_duration_minutes)
            consultation_cost = float(consultation_duration_minutes * 1.5) # consultation rate
            print('Consultation Cost: $', consultation_cost)


            # 6 Get prescription {prescription_id}
            # 7 Return prescription {prescription_id, prescription}
            print("\n\n")
            print("------------------------------STEP 6 & 7------------------------------")
            if prescription_id:
                print(f"\nFetching prescription details for ID: {prescription_id}...")
                prescription_result = invoke_http(f"{prescription_URL}/{prescription_id}", method='GET')
                medicine_list = prescription_result['prescription']["medicine"]
                print('Prescriptions:', medicine_list)
                
                if "error" in prescription_result:
                    print(f"Warning: Failed to retrieve prescription details: {prescription_result}")



            # 8 Check insurance {patient_id}
            # 9 Return insurance status {patient_id, patient_contact, patient_address, insurance}
            print("\n\n")
            print("------------------------------STEP 8 & 9------------------------------")
            print(f"\nFetching patient details for ID: {patient_id}...")
            patient_insurance = invoke_http(f"{patient_URL}/insurance/{patient_id}", method='GET')
            print('Patient insurance',patient_insurance)
  
            
            

  
            # 10 Get cost of medicine
            # 11 Return cost of medicine
            print("\n\n")
            print("------------------------------STEP 10 & 11------------------------------")
            
            calculate_medicines = invoke_http(f"{prescription_URL}/calculate_cost", method='POST', json={"medicines": medicine_list})
            total_cost =float(calculate_medicines['total_cost']) + consultation_cost
            print('Total Cost (consultation + medicine): $',total_cost)
           

            # 12 Create new payment request
            # 13 Return payment_id {payment_id, status}
            print("\n\n")
            print("------------------------------STEP 12 & 13------------------------------")

            payment_data = {
                "appointment_id": appointment_id,
                "payment_amount": total_cost,
                "insurance": patient_insurance['patient_insurance']

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
            
            
            # Return payment details {payment_id, payment_amount}
            return jsonify({
                "code": 200,
                "message": "Post-appointment (calculate) processing completed successfully",
                "data": {
                    "payment_id": payment_id,
                    "payment_amount": total_cost    
                }
            }), 200
        
        except Exception as e:
            print("ERROR:", str(e))
            return jsonify({"code": 500, "message": "Internal server error", "error": str(e)}), 500
            
        
    return jsonify({"code": 400, "message": "Invalid JSON input"}), 400



@app.route("/process/finish", methods=['POST'])
def process_appointment_finish():

    if request.is_json:
        try:
            # Extract data from the request
            data = request.get_json()
            print("\nReceived post-payment request:", data)
            appointment_id = data.get("appointment_id")
            payment_id = data.get("payment_id")
            payment_status  = data.get("payment_status")
            # 18 Update payment_status in payment
           
            print("\n\n")
            print("------------------------------STEP 18------------------------------")
            patch_result = invoke_http(f"{payment_URL}", method='PATCH', json={"payment_id": payment_id})
            print("Patch result:", patch_result)
            
            # 19 Update payment_id in appointment 
           
            print("\n\n")
            print("------------------------------STEP 19------------------------------")
            payment_update_payload = {
                "appointment_id": appointment_id,
                "payment_id": payment_id
            }
            print(f"\nFetching appointment details for ID: {appointment_id}...")
            update_result = invoke_http(f"{appointment_URL}/payment", method='PATCH', json=payment_update_payload)
            print("Payment update result:", update_result)
      

            
            # Return payment details {payment_id, payment_amount}
            return jsonify({
                "code": 200,
                "message": "Post-appointment (finish) processing completed successfully",
                
            }), 200
        
        except Exception as e:
            print("ERROR:", str(e))
            return jsonify({"code": 500, "message": "Internal server error", "error": str(e)}), 500
            
        
    return jsonify({"code": 400, "message": "Invalid JSON input"}), 400


if __name__ == "__main__":
    print("Starting process_appointment microservice...")
    app.run(host="0.0.0.0", port=5000, debug=True)


