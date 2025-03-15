from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Patient(db.Model):
    __tablename__ = 'patient'
    
    patientID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_contact = db.Column(db.Integer, nullable=False)
    insurance = db.Column(db.Boolean, default=False)
    patientName = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    patient_password = db.Column(db.String(100), nullable=False)
    allergies = db.Column(db.JSON, nullable=True)

    def json(self):
        return {
            "patient_id": self.patientID,
            "patient_contact": self.patient_contact,
            "insurance": self.insurance,
            "patient_name": self.patientName,
            "address": self.address,
            "allergies": self.allergies
        }


with app.app_context():
    db.create_all()


@app.route("/patient/authenticate/<int:patient_id>&<string:patient_password>", methods=['GET'])
def authenticate_patient(patient_id, patient_password):
    patient = Patient.query.filter_by(patientID=patient_id, patient_password=patient_password).first()
    if not patient:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({"patient_id": patient.patientID, "patient_name": patient.patientName}), 200


@app.route("/patient/allergies/<int:patient_id>", methods=['GET'])
def get_patient_allergies(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({"patient_id": patient.patientID, "allergies": patient.allergies}), 200


@app.route("/patient/insurance/<int:patient_id>", methods=['GET'])
def get_patient_insurance(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({
        "patient_id": patient.patientID,
        "patient_contact": patient.patient_contact,
        "patient_address": patient.address,
        "insurance": patient.insurance
    }), 200


@app.route("/patient", methods=['POST'])
def create_patient():
    data = request.get_json()
    if not data or not all(key in data for key in ["patient_contact", "patient_name", "address", "patient_password"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_patient = Patient(
        patient_contact=data["patient_contact"],
        insurance=data.get("insurance", False),
        patientName=data["patient_name"],
        address=data["address"],
        patient_password=data["patient_password"],
        allergies=data.get("allergies", [])
    )

    try:
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({"message": "Patient created successfully", "patient_id": new_patient.patientID}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/patient/<int:patient_id>", methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    data = request.get_json()
    if "patient_contact" in data:
        patient.patient_contact = data["patient_contact"]
    if "insurance" in data:
        patient.insurance = data["insurance"]
    if "patient_name" in data:
        patient.patientName = data["patient_name"]
    if "address" in data:
        patient.address = data["address"]
    if "patient_password" in data:
        patient.patient_password = data["patient_password"]
    if "allergies" in data:
        patient.allergies = data["allergies"]

    try:
        db.session.commit()
        return jsonify({"message": "Patient updated successfully", "patient": patient.json()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/patient/<int:patient_id>", methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    try:
        db.session.delete(patient)
        db.session.commit()
        return jsonify({"message": "Patient deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
