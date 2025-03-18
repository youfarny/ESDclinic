from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@116.15.73.191:3306/queue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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
    doctor_counts = db.session.query(Queue.doctor_id, db.func.count(Queue.appointment_id).label("queue_length")) \
                              .group_by(Queue.doctor_id) \
                              .order_by("queue_length").first()

    if not doctor_counts:
        return jsonify({"error": "No doctors in queue"}), 404

    return jsonify({"doctor_id": doctor_counts.doctor_id, "queue_length": doctor_counts.queue_length}), 200


@app.route("/queue", methods=['POST'])
def create_appointment():
    data = request.get_json()
    if not data or "doctor_id" not in data or "patient_contact" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_appointment = Queue(
        doctor_id=data["doctor_id"],
        patient_contact=data["patient_contact"]
    )

    try:
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({"appointment_id": new_appointment.appointment_id, "queue_length": db.session.query(Queue).filter_by(doctor_id=data["doctor_id"]).count()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/queue/next_start/<int:doctor_id>", methods=['GET'])
def get_next_start(doctor_id):
    next_patient = Queue.query.filter_by(doctor_id=doctor_id).order_by(Queue.appointment_id).first()
    if not next_patient:
        return jsonify({"error": "No patients in queue"}), 404

    return jsonify({"doctor_id": next_patient.doctor_id, "appointment_id": next_patient.appointment_id}), 200


@app.route("/queue/next_end/<int:doctor_id>", methods=['GET'])
def get_next_end(doctor_id):
    next_patient = Queue.query.filter_by(doctor_id=doctor_id).order_by(Queue.appointment_id).first()
    if not next_patient:
        return jsonify({"error": "No patients in queue"}), 404

    return jsonify({
        "doctor_id": next_patient.doctor_id,
        "appointment_id": next_patient.appointment_id,
        "patient_contact": next_patient.patient_contact
    }), 200


@app.route("/queue/<int:doctor_id>/<int:appointment_id>", methods=['DELETE'])
def delete_queue_entry(doctor_id, appointment_id):
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
