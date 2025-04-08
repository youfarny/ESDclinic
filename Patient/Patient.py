from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])



# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@116.15.73.191:3306/patient'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Swagger
swagger = Swagger(app)

class Patient(db.Model):
    __tablename__ = 'patient'

    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_password = db.Column(db.String(100), nullable=False)
    patient_contact = db.Column(db.Integer, nullable=False)
    patient_address = db.Column(db.String(200), nullable=False)
    patient_insurance = db.Column(db.Boolean, default=False)
    patient_allergies = db.Column(db.JSON, nullable=True)
    patient_age = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            "patient_id": self.patient_id,
            "patient_contact": self.patient_contact,
            "patient_insurance": self.patient_insurance,
            "patient_name": self.patient_name,
            "patient_address": self.patient_address,
            "patient_allergies": self.patient_allergies,
            "patient_age": self.patient_age
        }

with app.app_context():
    db.create_all()

@app.route("/patient/authenticate/<int:patient_id>&<string:patient_password>", methods=['GET'])
def authenticate_patient(patient_id, patient_password):
    """
    Authenticate a patient using patient_id and password
    ---
    tags:
      - Patient
    parameters:
      - name: patient_id
        in: path
        type: integer
        required: true
        description: The patient's unique ID
      - name: patient_password
        in: path
        type: string
        required: true
        description: The patient's password
    responses:
      200:
        description: Patient successfully authenticated
        schema:
          type: object
          properties:
            patient_id:
              type: integer
            patient_name:
              type: string
      401:
        description: Invalid credentials
    """
    patient = Patient.query.filter_by(patient_id=patient_id, patient_password=patient_password).first()
    if not patient:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({"patient_id": patient.patient_id, "patient_name": patient.patient_name}), 200

@app.route("/patient/<int:patient_id>", methods=['GET'])
def get_patient(patient_id):
    """
    Get a patient's allergy information
    ---
    tags:
      - Patient
    parameters:
      - name: patient_id
        in: path
        required: true
        description: The patient's unique ID
        schema:
          type: integer
          example: 123
    responses:
      200:
        description: A list of the patient's allergies
        content:
          application/json:
            schema:
              type: object
              properties:
                patient_id:
                  type: integer
                  example: 123
                allergies:
                  type: array
                  items:
                    type: string
                  example: ["Peanuts", "Shellfish"]
      404:
        description: Patient not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Patient not found
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify(patient.json()), 200


@app.route("/patient/allergies/<int:patient_id>", methods=['GET'])
def get_patient_allergies(patient_id):
    """
    Get a patient's allergies
    ---
    tags:
      - Patient
    parameters:
      - name: patient_id
        in: path
        type: integer
        required: true
        description: The patient's unique ID
    responses:
      200:
        description: A list of the patient's allergies
        schema:
          type: object
          properties:
            patient_id:
              type: integer
            allergies:
              type: array
              items:
                type: string
      404:
        description: Patient not found
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({"patient_id": patient.patient_id, "allergies": patient.patient_allergies, "patient_age": patient.patient_age}), 200

@app.route("/patient/contact/<int:patient_id>", methods=['GET'])
def get_patient_contact(patient_id):
    """
    Get a patient's contact details
    ---
    tags:
      - Patient
    parameters:
      - name: patient_id
        in: path
        type: integer
        required: true
        description: The patient's unique ID
    responses:
      200:
        description: Patient contact details retrieved successfully
        schema:
          type: object
          properties:
            patient_id:
              type: integer
            patient_contact:
              type: string
      404:
        description: Patient not found
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({"patient_id": patient.patient_id, "patient_contact": patient.patient_contact}), 200

@app.route("/patient/insurance/<int:patient_id>", methods=['GET'])
def get_patient_insurance(patient_id):
    """
    Get a patient's insurance details
    ---
    tags:
      - Patient
    parameters:
      - name: patient_id
        in: path
        type: integer
        required: true
        description: The patient's unique ID
    responses:
      200:
        description: The patient's insurance details
        schema:
          type: object
          properties:
            patient_id:
              type: integer
            patient_contact:
              type: integer
            patient_address:
              type: string
            patient_insurance:
              type: boolean
      404:
        description: Patient not found
    """
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
    """
    Create a new patient
    ---
    tags:
      - Patient
    parameters:
      - name: body
        in: body
        required: true
        description: Patient data to create
        schema:
          type: object
          properties:
            patient_contact:
              type: integer
            patient_name:
              type: string
            patient_address:
              type: string
            patient_password:
              type: string
            patient_insurance:
              type: boolean
            patient_allergies:
              type: array
              items:
                type: string
    responses:
      201:
        description: Patient created successfully
        schema:
          type: object
          properties:
            message:
              type: string
            patient_id:
              type: integer
      400:
        description: Missing required fields
    """
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
    """
    Update patient details
    ---
    tags:
      - Patient
    parameters:
      - name: patient_id
        in: path
        type: integer
        required: true
        description: The patient's unique ID
      - name: body
        in: body
        required: true
        description: Updated patient data
        schema:
          type: object
          properties:
            patient_contact:
              type: integer
            patient_insurance:
              type: boolean
            patient_name:
              type: string
            patient_address:
              type: string
            patient_password:
              type: string
            patient_allergies:
              type: array
              items:
                type: string
    responses:
      200:
        description: Patient updated successfully
      404:
        description: Patient not found
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    data = request.get_json()
    if "patient_contact" in data:
        patient.patient_contact = data["patient_contact"]
    if "patient_insurance" in data:
        patient.patient_insurance = data["patient_insurance"]
    if "patient_name" in data:
        patient.patient_name = data["patient_name"]
    if "patient_address" in data:
        patient.patient_address = data["patient_address"]
    if "patient_password" in data:
        patient.patient_password = data["patient_password"]
    if "patient_allergies" in data:
        patient.patient_allergies = data["patient_allergies"]
    if "patient_age" in data:
        patient.patient_age = data["patient_age"]

    try:
        db.session.commit()
        return jsonify({"message": "Patient updated successfully", "patient": patient.json()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/patient/<int:patient_id>", methods=['DELETE'])
def delete_patient(patient_id):
    """
    Delete a patient by ID
    ---
    tags:
      - Patient
    parameters:
      - name: patient_id
        in: path
        type: integer
        required: true
        description: The patient's unique ID
    responses:
      200:
        description: Patient deleted successfully
      404:
        description: Patient not found
    """
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
