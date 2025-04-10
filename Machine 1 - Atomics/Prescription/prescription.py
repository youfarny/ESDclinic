from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])


# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@202.166.134.237:3306/prescription'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Swagger
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "SMUDOC Prescription API",
        "description": "API documentation for managing prescriptions and medicine costs in SMUDOC",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"],
    "tags": [
        {
            "name": "Prescription",
            "description": "Endpoints for handling prescriptions"
        },
        {
            "name": "Medicine",
            "description": "Endpoints for retrieving and calculating medicine costs"
        }
    ],
    "definitions": {
        "Prescription": {
            "type": "object",
            "properties": {
                "prescription_id": {
                    "type": "integer",
                    "example": 1,
                    "description": "Unique ID for the prescription"
                },
                "medicine": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "example": ["flu", "cough"],
                    "description": "List of medicines prescribed"
                },
                "appointment_id": {
                    "type": "integer",
                    "example": 123,
                    "description": "Associated appointment ID"
                }
            }
        },
        "Medicine": {
            "type": "object",
            "properties": {
                "indiv_medicine": {
                    "type": "string",
                    "example": "paracetamol",
                    "description": "Name of the medicine"
                },
                "cost": {
                    "type": "number",
                    "format": "float",
                    "example": 12.5,
                    "description": "Cost of the medicine"
                }
            }
        }
    }
})

class Prescription(db.Model):
    __tablename__ = 'prescription'
    
    prescription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medicine = db.Column(db.JSON, nullable=False)
    appointment_id = db.Column(db.Integer, nullable=False)

    def json(self):
        return {"prescription_id": self.prescription_id, "medicine": self.medicine, "appointment_id": self.appointment_id}

class Medicine(db.Model):
    __tablename__ = 'medicine'
    
    indiv_medicine = db.Column(db.String(100), primary_key=True, nullable=True)
    cost = db.Column(db.Float, nullable=False)

    def json(self):
        return {"indiv_medicine": self.indiv_medicine, "cost": self.cost}

with app.app_context():
    db.create_all()

@app.route("/medicine/<string:medicine_name>", methods=['GET'])
def get_medicine_cost(medicine_name):
    """
    Get the cost of a specific medicine
    ---
    tags:
      - Medicine
    parameters:
      - name: medicine_name
        in: path
        type: string
        required: true
        description: The name of the medicine to retrieve the cost for
    responses:
      200:
        description: Medicine cost retrieved successfully
        schema:
          type: object
          properties:
            medicine:
              type: string
            cost:
              type: integer
      404:
        description: Medicine not found
    """
    medicine = Medicine.query.get(medicine_name)
    if not medicine:
        return jsonify({"error": "Medicine not found"}), 404

    return jsonify({"medicine": medicine.indiv_medicine, "cost": medicine.cost}), 200

@app.route("/prescription/calculate_cost", methods=['POST'])
def calculate_medicine_cost():
    """
    Calculate total cost of multiple medicines
    ---
    tags:
      - Medicine
    parameters:
      - name: body
        in: body
        required: true
        description: List of medicines in JSON format
        schema:
          type: object
          properties:
            medicines:
              type: array
              items:
                type: string
              example: ["cough", "flu", "fever"]
    responses:
      200:
        description: Total cost calculated successfully
        schema:
          type: object
          properties:
            total_cost:
              type: integer
      400:
        description: Invalid medicine list
    """
    data = request.get_json()
    if 'medicines' not in data or not isinstance(data['medicines'], list):
        return jsonify({"error": "Invalid medicine list"}), 400

    total_cost = 0

    for med in data['medicines']:
        medicine = Medicine.query.get(med)
        # if medicine:
        #     total_cost += medicine.cost
        # else:
        #     return jsonify({"error": f"Medicine '{med}' not found"}), 404
        try:
            total_cost += medicine.cost
        except:
            print("Medicine not in pricelist")

    return jsonify({"total_cost": total_cost}), 200

@app.route("/prescription", methods=['POST'])
def create_prescription():
    """
    Create a new prescription
    ---
    tags:
      - Prescription
    parameters:
      - name: body
        in: body
        required: true
        description: Prescription data to create a new prescription
        schema:
          type: object
          properties:
            medicine:
              type: string
            appointment_id:
              type: integer
    responses:
      201:
        description: Prescription successfully created
        schema:
          type: object
          properties:
            prescription_id:
              type: integer
      400:
        description: Missing medicine or appointment_id
    """
    data = request.get_json()
    if not data or 'medicine' not in data or 'appointment_id' not in data:
        return jsonify({"error": "Missing medicine or appointment_id"}), 400

    new_prescription = Prescription(medicine=data['medicine'], appointment_id=data['appointment_id'])
    
    try:
        db.session.add(new_prescription)
        db.session.commit()
        return jsonify({"prescription_id": new_prescription.prescription_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/prescription", methods=['GET'])
def get_all_prescriptions():
    """
    Get all prescriptions
    ---
    tags:
      - Prescription
    responses:
      200:
        description: A list of all prescriptions
        schema:
          type: object
          properties:
            prescriptions:
              type: array
              items:
                $ref: '#/definitions/Prescription'
      404:
        description: No prescriptions found
    """
    prescriptions = Prescription.query.all()
    if not prescriptions:
        return jsonify({"message": "No prescriptions found"}), 404

    return jsonify({"prescriptions": [prescription.json() for prescription in prescriptions]}), 200

@app.route("/prescription/<int:prescription_id>", methods=['GET'])
def get_prescription(prescription_id):
    """
    Get a specific prescription by ID
    ---
    tags:
      - Prescription
    parameters:
      - name: prescription_id
        in: path
        type: integer
        required: true
        description: The prescription ID to retrieve
    responses:
      200:
        description: The prescription details
        schema:
          $ref: '#/definitions/Prescription'
      404:
        description: Prescription not found
    """
    prescription = Prescription.query.get(prescription_id)
    if not prescription:
        return jsonify({"error": "Prescription not found"}), 404

    return jsonify({"prescription": prescription.json()}), 200

@app.route("/prescription/<int:prescription_id>", methods=['PUT'])
def update_prescription(prescription_id):
    """
    Update a prescription
    ---
    tags:
      - Prescription
    parameters:
      - name: prescription_id
        in: path
        type: integer
        required: true
        description: The prescription ID to update
      - name: body
        in: body
        required: true
        description: The updated prescription data
        schema:
          type: object
          properties:
            medicine:
              type: string
            appointment_id:
              type: integer
    responses:
      200:
        description: Prescription updated successfully
        schema:
          $ref: '#/definitions/Prescription'
      404:
        description: Prescription not found
    """
    prescription = Prescription.query.get(prescription_id)
    if not prescription:
        return jsonify({"error": "Prescription not found"}), 404

    data = request.get_json()
    if 'medicine' in data:
        prescription.medicine = data['medicine']
    if 'appointment_id' in data:
        prescription.appointment_id = data['appointment_id']

    try:
        db.session.commit()
        return jsonify({"message": "Prescription updated successfully", "prescription": prescription.json()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/prescription/<int:prescription_id>", methods=['DELETE'])
def delete_prescription(prescription_id):
    """
    Delete a prescription by ID
    ---
    tags:
      - Prescription
    parameters:
      - name: prescription_id
        in: path
        type: integer
        required: true
        description: The prescription ID to delete
    responses:
      200:
        description: Prescription deleted successfully
      404:
        description: Prescription not found
    """
    prescription = Prescription.query.get(prescription_id)
    if not prescription:
        return jsonify({"error": "Prescription not found"}), 404

    try:
        db.session.delete(prescription)
        db.session.commit()
        return jsonify({"message": "Prescription deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5104)
