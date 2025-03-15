from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@116.15.73.191:3306/prescription'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Prescription(db.Model):
    __tablename__ = 'prescription'
    
    prescriptionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medicine = db.Column(db.String(100), nullable=False)
    appointmentID = db.Column(db.Integer, nullable=False)

    def json(self):
        return {"prescription_id": self.prescriptionID, "medicine": self.medicine, "appointment_id": self.appointmentID}


with app.app_context():
    db.create_all()


@app.route("/new", methods=['POST'])
def create_prescription():
    data = request.get_json()
    if not data or 'medicine' not in data or 'appointment_id' not in data:
        return jsonify({"error": "Missing medicine or appointment_id"}), 400

    new_prescription = Prescription(medicine=data['medicine'], appointmentID=data['appointment_id'])
    
    try:
        db.session.add(new_prescription)
        db.session.commit()
        return jsonify({"prescription_id": new_prescription.prescriptionID}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

@app.route("/prescriptions", methods=['GET'])
def get_all_prescriptions():
    prescriptions = Prescription.query.all()
    if not prescriptions:   
        return jsonify({"message": "No prescriptions found"}), 404

    return jsonify({"prescriptions": [prescription.json() for prescription in prescriptions]}), 200



@app.route("/prescription/<int:prescription_id>", methods=['GET'])
def get_prescription(prescription_id):
    prescription = Prescription.query.get(prescription_id)
    if not prescription:
        return jsonify({"error": "Prescription not found"}), 404

    return jsonify({"prescription": prescription.json()}), 200


@app.route("/prescription/<int:prescription_id>", methods=['PUT'])
def update_prescription(prescription_id):
    prescription = Prescription.query.get(prescription_id)
    if not prescription:
        return jsonify({"error": "Prescription not found"}), 404

    data = request.get_json()
    if 'medicine' in data:
        prescription.medicine = data['medicine']
    if 'appointment_id' in data:
        prescription.appointmentID = data['appointment_id']

    try:
        db.session.commit()
        return jsonify({"message": "Prescription updated successfully", "prescription": prescription.json()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/prescription/<int:prescription_id>", methods=['DELETE'])
def delete_prescription(prescription_id):
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
    app.run(debug=True, host='0.0.0.0', port=5004)
