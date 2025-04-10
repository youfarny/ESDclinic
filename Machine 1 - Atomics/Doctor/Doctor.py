from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@116.15.73.191:3306/doctor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

swagger = Swagger(app)


class Doctor(db.Model):
    __tablename__ = 'doctor'
    
    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_name = db.Column(db.String(100), nullable=False)

    def json(self):
        return {"doctor_id": self.doctor_id, "doctor_name": self.doctor_name}


# with app.app_context():
#     print("Trying to connect to MySQL...")
#     db.create_all()
#     print("Database initialized successfully.")
#     db.create_all()

@app.route("/doctor", methods=['POST'])
def create_doctor():
    """
    Create a new doctor
    ---
    tags:
      - Doctor
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - doctor_name
          properties:
            doctor_name:
              type: string
              example: "Dr. John Doe"
    responses:
      201:
        description: The doctor was successfully created
        schema:
          id: Doctor
          properties:
            doctor_id:
              type: integer
              description: The doctor ID
              example: 1
    """
    data = request.get_json()
    if not data or 'doctor_name' not in data:
        return jsonify({"error": "Missing doctor_name"}), 400

    new_doctor = Doctor(doctor_name=data['doctor_name'])

    try:
        db.session.add(new_doctor)
        db.session.commit()
        return jsonify({"doctor_id": new_doctor.doctor_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/doctor/<int:doctor_id>", methods=['GET'])
def get_doctor_by_id(doctor_id):
    """
    Get a doctor by ID
    ---
    tags:
      - Doctor
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
        description: The doctor ID to retrieve
    responses:
      200:
        description: A single doctor
        schema:
          id: Doctor
          properties:
            doctor_id:
              type: integer
              description: The doctor ID
              example: 1
            doctor_name:
              type: string
              description: The name of the doctor
              example: "Dr. John Doe"
      404:
        description: Doctor not found
    """
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    return jsonify({"doctor": doctor.json()}), 200

@app.route("/doctor_name/<string:doctor_name>", methods=['GET'])
def get_doctor_by_name(doctor_name):
    """
    Get a doctor by name
    ---
    tags:
      - Doctor
    parameters:
      - name: doctor_name
        in: path
        type: string
        required: true
        description: The name of the doctor to search for
    responses:
      200:
        description: A single doctor
        schema:
          id: Doctor
          properties:
            doctor_id:
              type: integer
              description: The doctor ID
              example: 1
            doctor_name:
              type: string
              description: The name of the doctor
              example: "Dr. John Doe"
      404:
        description: Doctor not found
    """
    doctor = Doctor.query.filter_by(doctor_name=doctor_name).first()
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    return jsonify({"doctor": doctor.json()}), 200


@app.route("/doctors", methods=['GET'])
def get_all_doctors():
    """
    Get all doctors
    ---
    tags:
      - Doctor
    responses:
      200:
        description: A list of all doctors
        schema:
          id: DoctorList
          properties:
            doctors:
              type: array
              items:
                $ref: '#/definitions/Doctor'
      404:
        description: No doctors found
    """
    doctors = Doctor.query.all()
    if not doctors:
        return jsonify({"message": "No doctors found"}), 404

    return jsonify({"doctors": [doctor.json() for doctor in doctors]}), 200


@app.route("/doctor/<int:doctor_id>", methods=['PUT'])
def update_doctor(doctor_id):
    """
    Update a doctor's information
    ---
    tags:
      - Doctor
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
        description: The doctor ID to update
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - doctor_name
          properties:
            doctor_name:
              type: string
              example: "Dr. John Doe"
    responses:
      200:
        description: The doctor was updated
        schema:
          id: Doctor
          properties:
            doctor_id:
              type: integer
              description: The doctor ID
              example: 1
            doctor_name:
              type: string
              description: The name of the doctor
              example: "Dr. John Smith"
      404:
        description: Doctor not found
    """
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    data = request.get_json()
    if 'doctor_name' in data:
        doctor.doctor_name = data['doctor_name']

    try:
        db.session.commit()
        return jsonify({"message": "Doctor updated successfully", "doctor": doctor.json()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/doctor/<int:doctor_id>", methods=['DELETE'])
def delete_doctor(doctor_id):
    """
    Delete a doctor by ID
    ---
    tags:
      - Doctor
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
        description: The doctor ID to delete
    responses:
      200:
        description: The doctor was deleted
      404:
        description: Doctor not found
    """
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    try:
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({"message": "Doctor deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5101)
