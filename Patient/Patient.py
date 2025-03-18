from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@116.15.73.191:3306/patient'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Patient(db.Model):
    __tablename__ = 'patient'
    
    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_password = db.Column(db.String(100), nullable=False)
    patient_contact = db.Column(db.Integer, nullable=False)
    patient_address = db.Column(db.String(200), nullable=False)
    patient_insurance = db.Column(db.Boolean, default=False)
    patient_allergies = db.Column(db.JSON, nullable=True)

    def json(self):
        return {
            "patient_id": self.patient_id,
            "patient_contact": self.patient_contact,
            "patient_insurance": self.patient_insurance,
            "patient_name": self.patient_name,
            "patient_address": self.patient_address,
            "patient_allergies": self.patient_allergies
        }


with app.app_context():
    db.create_all()


@app.route("/patient/authenticate/<int:patient_id>&<string:patient_password>", methods=['GET'])
def authenticate_patient(patient_id, patient_password):
    patient = Patient.query.filter_by(patient_id=patient_id, patient_password=patient_password).first()
    if not patient:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({"patient_id": patient.patient_id, "patient_name": patient.patient_name}), 200


@app.route("/patient/allergies/<int:patient_id>", methods=['GET'])
def get_patient_allergies(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({"patient_id": patient.patient_id, "allergies": patient.patient_allergies}), 200


@app.route("/patient/insurance/<int:patient_id>", methods=['GET'])
def get_patient_insurance(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({
        "patient_id": patient.patient_id,
        "patient_contact": patient.patient_contact,
        "patient_address": patient.patient_address,
        "patient_insurance": patient.patient_insurance
    }), 200


@app.route("/patient", methods=['POST'])
def create_patient():
    data = request.get_json()
    if not data or not all(key in data for key in ["patient_contact", "patient_name", "patient_address", "patient_password"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_patient = Patient(
        patient_contact=data["patient_contact"],
        patient_insurance=data.get("patient_insurance", False),
        patient_name=data["patient_name"],
        patient_address=data["patient_address"],
        patient_password=data["patient_password"],
        patient_allergies=data.get("patient_allergies", [])
    )

    try:
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({"message": "Patient created successfully", "patient_id": new_patient.patient_id}), 201
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
    if "patient_insurance" in data:
        patient.insurance = data["patient_insurance"]
    if "patient_name" in data:
        patient.patientName = data["patient_name"]
    if "patient_address" in data:
        patient.address = data["patient_address"]
    if "patient_password" in data:
        patient.patient_password = data["patient_password"]
    if "patient_allergies" in data:
        patient.allergies = data["patient_allergies"]

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
    app.run(debug=True, host='0.0.0.0', port=5102)
