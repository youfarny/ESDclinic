from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@116.15.73.191:3306/appointment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Swagger
swagger = Swagger(app)

# Appointment Model
class Appointment(db.Model):
    __tablename__ = 'appointment'

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    patient_symptoms = db.Column(db.JSON, nullable=False)
    notes = db.Column(db.JSON)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    diagnosis = db.Column(db.String(500))
    prescription_id = db.Column(db.Integer)
    payment_id = db.Column(db.Integer)

    def json(self):
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "patient_symptoms": self.patient_symptoms,
            "notes": self.notes,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "diagnosis": self.diagnosis,
            "prescription_id": self.prescription_id,
            "payment_id": self.payment_id
        }

# Initialize Database
with app.app_context():
    db.create_all()

# Get Patient Records
@app.route("/appointment/records/<int:patient_id>", methods=['GET'])
def get_patient_appointments(patient_id):
    """
    Get all appointments for a patient
    ---
    tags:
      - Appointment
    parameters:
      - name: patient_id
        in: path
        type: integer
        required: true
        description: The patient ID to fetch appointments
    responses:
      200:
        description: A list of appointments for the patient
        schema:
          type: array
          items:
            $ref: '#/definitions/Appointment'
      404:
        description: No appointments found
    """
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    if not appointments:
        return jsonify({"message": "No appointments found"}), 404
    return jsonify([appointment.json() for appointment in appointments]), 200

# Create New Appointment
@app.route("/appointment/new", methods=['POST'])
def create_appointment():
    """
    Create a new appointment
    ---
    tags:
      - Appointment
    parameters:
      - name: body
        in: body
        required: true
        description: Appointment data to create
        schema:
          type: object
          properties:
            patient_id:
              type: integer
            doctor_id:
              type: integer
            patient_symptoms:
              type: string
    responses:
      201:
        description: Appointment successfully created
        schema:
          type: object
          properties:
            appointment_id:
              type: integer
      400:
        description: Missing required fields
    """
    data = request.get_json()
    if not data or 'patient_id' not in data or 'doctor_id' not in data or 'patient_symptoms' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_appointment = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        patient_symptoms=data['patient_symptoms']
    )

    try:
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({"appointment_id": new_appointment.appointment_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Retrieve Appointment
@app.route("/appointment/<int:appointment_id>", methods=['GET'])
def get_appointment(appointment_id):
    """
    Retrieve a specific appointment
    ---
    tags:
      - Appointment
    parameters:
      - name: appointment_id
        in: path
        type: integer
        required: true
        description: The appointment ID to retrieve
    responses:
      200:
        description: Appointment details
        schema:
          $ref: '#/definitions/Appointment'
      404:
        description: Appointment not found
    """
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(appointment.json()), 200

# Start Appointment
@app.route("/appointment/appointment_start", methods=['PATCH'])
def start_appointment():
    """
    Start an appointment and add notes
    ---
    tags:
      - Appointment
    parameters:
      - name: body
        in: body
        required: true
        description: Start appointment data
        schema:
          type: object
          properties:
            appointment_id:
              type: integer
            notes:
              type: JSON
            startTime:
              type: string
              format: date-time
    responses:
      200:
        description: Appointment started successfully
      400:
        description: Missing required fields
    """
    data = request.get_json()
        # not sure if we still integrating the external recommendations api so ill just put notes first 
    # also assuming that the doctor keys in the start time himself? or should we set timer for this? 

    if "appointment_id" not in data or "notes" not in data or "startTime" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    appointment = Appointment.query.get(data["appointment_id"])
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    appointment.notes = data["notes"]
    appointment.start_time = data["startTime"]

    try:
        db.session.commit()
        return jsonify({"message": "Appointment started successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# End Appointment - update appointment details
@app.route("/appointment/appointment_end", methods=['PATCH'])
def end_appointment():
    """
    End an appointment and update details
    ---
    tags:
      - Appointment
    parameters:
      - name: body
        in: body
        required: true
        description: End appointment data
        schema:
          type: object
          properties:
            appointment_id:
              type: integer
            end_time:
              type: string
              format: date-time
            diagnosis:
              type: string
            prescription_id:
              type: integer
    responses:
      200:
        description: Appointment updated successfully
      400:
        description: Missing required fields
    """
    data = request.get_json()
    if "appointment_id" not in data or "end_time" not in data or "diagnosis" not in data or "prescription_id" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    appointment = Appointment.query.get(data["appointment_id"])
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    appointment.end_time = data["end_time"]
    appointment.diagnosis = data["diagnosis"]
    appointment.prescription_id = data["prescription_id"]

    try:
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Payment success
@app.route("/appointment/payment", methods=['PATCH'])
def payment_success():
    """
    Mark payment as successful
    ---
    tags:
      - Appointment
    parameters:
      - name: body
        in: body
        required: true
        description: Payment success data
        schema:
          type: object
          properties:
            appointment_id:
              type: integer
            payment_id:
              type: integer
    responses:
      200:
        description: Payment successfully processed
      400:
        description: Missing required fields
    """
    data = request.get_json()
    if "appointment_id" not in data or "payment_id" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    appointment = Appointment.query.get(data["appointment_id"])
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    appointment.payment_id = data["payment_id"]

    try:
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5100)
