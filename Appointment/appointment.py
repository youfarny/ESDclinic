from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@116.15.73.191:3306/appointment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Appointment Model
class Appointment(db.Model):
    __tablename__ = 'appointment'

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    patient_symptoms = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.String(500))
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
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    if not appointments:
        return jsonify({"message": "No appointments found"}), 404
    return jsonify([appointment.json() for appointment in appointments]), 200

# Create New Appointment
@app.route("/appointment/new", methods=['POST'])
def create_appointment():
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
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(appointment.json()), 200

# Start Appointment

@app.route("/appointment/appointment_start", methods=['PATCH'])
def start_appointment():
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

