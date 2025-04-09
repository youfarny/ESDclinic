from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])  # your Vue frontend

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@116.15.73.191:3306/queue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Swagger
swagger = Swagger(app)

class Queue(db.Model):
    __tablename__ = 'queue'
    
    doctor_id = db.Column(db.Integer, nullable=False)
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_contact = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            "doctor_id": self.doctor_id,
            "appointment_id": self.appointment_id,
            "patient_contact": self.patient_contact
        }

with app.app_context():
    db.create_all()

@app.route("/queue/shortest", methods=['GET'])
def get_shortest_queue():
    """
    Get the doctor with the shortest queue
    ---
    tags:
      - Queue
    responses:
      200:
        description: The doctor with the shortest queue
        schema:
          type: object
          properties:
            doctor_id:
              type: integer
            queue_length:
              type: integer
      404:
        description: No doctors in queue
    """
    doctor_counts = db.session.query(Queue.doctor_id, db.func.count(Queue.appointment_id).label("queue_length")) \
                              .group_by(Queue.doctor_id) \
                              .order_by("queue_length").first()

    if not doctor_counts:
        return jsonify({"error": "No doctors in queue"}), 404

    return jsonify({"doctor_id": doctor_counts.doctor_id, "queue_length": doctor_counts.queue_length}), 200


@app.route("/queue", methods=['POST'])
def create_appointment():
    """
    Create a new appointment in the queue
    ---
    tags:
      - Queue
    parameters:
      - name: body
        in: body
        required: true
        description: Appointment data to add to the queue
        schema:
          type: object
          properties:
            doctor_id:
              type: integer
            patient_contact:
              type: integer
    responses:
      201:
        description: Appointment created successfully
        schema:
          type: object
          properties:
            appointment_id:
              type: integer
            queue_length:
              type: integer
      400:
        description: Missing required fields
    """
    data = request.get_json()
    if not data or "doctor_id" not in data or "patient_contact" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_appointment = Queue(
        appointment_id=data["appointment_id"],
        doctor_id=data["doctor_id"],
        patient_contact=data["patient_contact"]
    )

    try:
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({"appointment_id": new_appointment.appointment_id, "queue_length": db.session.query(Queue).filter_by(doctor_id=data["doctor_id"]).count()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/queue/next/<int:doctor_id>", methods=['GET'])
def get_next_start(doctor_id):
    """
    Get the next patient in the queue for a specific doctor (starting point)
    ---
    tags:
      - Queue
    parameters:
      - name: doctor_id
        in: path
        required: true
        type: integer
        description: The doctor's ID
    responses:
      200:
        description: The next patient in the queue
        schema:
          type: object
          properties:
            doctor_id:
              type: integer
            appointment_id:
              type: integer
      404:
        description: No patients in queue
    """
    next_patient = Queue.query.filter_by(doctor_id=doctor_id).order_by(Queue.appointment_id).first()
    if not next_patient:
        return jsonify({"error": "No patients in queue"}), 404

    return jsonify({"doctor_id": next_patient.doctor_id, "appointment_id": next_patient.appointment_id}), 200


# @app.route("/queue/next_end/<int:doctor_id>", methods=['GET'])
# def get_next_end(doctor_id):
#     """
#     Get the next patient in the queue for a specific doctor (end point)
#     ---
#     tags:
#       - Queue
#     parameters:
#       - name: doctor_id
#         in: path
#         required: true
#         type: integer
#         description: The doctor's ID
#     responses:
#       200:
#         description: The next patient in the queue
#         schema:
#           type: object
#           properties:
#             doctor_id:
#               type: integer
#             appointment_id:
#               type: integer
#             patient_contact:
#               type: integer
#       404:
#         description: No patients in queue
#     """
#     next_patient = Queue.query.filter_by(doctor_id=doctor_id).order_by(Queue.appointment_id).first()
#     if not next_patient:
#         return jsonify({"error": "No patients in queue"}), 404

#     return jsonify({
#         "doctor_id": next_patient.doctor_id,
#         "appointment_id": next_patient.appointment_id,
#         "patient_contact": next_patient.patient_contact
#     }), 200


@app.route("/queue/<int:doctor_id>/<int:appointment_id>", methods=['DELETE'])
def delete_queue_entry(doctor_id, appointment_id):
    """
    Delete a queue entry
    ---
    tags:
      - Queue
    parameters:
      - name: doctor_id
        in: path
        required: true
        type: integer
        description: The doctor's ID
      - name: appointment_id
        in: path
        required: true
        type: integer
        description: The appointment ID to delete
    responses:
      200:
        description: Queue entry deleted successfully
      404:
        description: Queue entry not found
    """
    queue_entry = Queue.query.filter_by(doctor_id=doctor_id, appointment_id=appointment_id).first()
    if not queue_entry:
        return jsonify({"error": "Queue entry not found"}), 404

    try:
        db.session.delete(queue_entry)
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5103)
