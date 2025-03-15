from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@116.15.73.191:3306/doctor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Doctor(db.Model):
    __tablename__ = 'doctor'
    
    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_name = db.Column(db.String(100), nullable=False)

    def json(self):
        return {"doctor_id": self.doctor_id, "doctor_name": self.doctor_name}


with app.app_context():
    db.create_all()


@app.route("/doctor", methods=['POST'])
def create_doctor():
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
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    return jsonify({"doctor": doctor.json()}), 200

@app.route("/doctor_name/<string:doctor_name>", methods=['GET'])
def get_doctor_by_name(doctor_name):
    doctor = Doctor.query.filter_by(doctor_name=doctor_name).first()
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    return jsonify({"doctor": doctor.json()}), 200


@app.route("/doctors", methods=['GET'])
def get_all_doctors():
    doctors = Doctor.query.all()
    if not doctors:
        return jsonify({"message": "No doctors found"}), 404

    return jsonify({"doctors": [doctor.json() for doctor in doctors]}), 200


@app.route("/doctor/<int:doctor_id>", methods=['PUT'])

def update_doctor(doctor_id):
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
    app.run(debug=True, host='0.0.0.0', port=5001)
