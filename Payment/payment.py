from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Payment(db.Model):
    __tablename__ = 'payment'
    
    paymentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointmentID = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=False)  # False means not paid, True means paid
    paymentAmount = db.Column(db.Float, nullable=False)

    def json(self):
        return {
            "payment_id": self.paymentID,
            "appointment_id": self.appointmentID,
            "status": self.status,
            "payment_amount": self.paymentAmount
        }


with app.app_context():
    db.create_all()


@app.route("/payment", methods=['POST'])
def create_payment():
    data = request.get_json()
    if not data or 'appointment_id' not in data or 'payment_amount' not in data:
        return jsonify({"error": "Missing appointment_id or payment_amount"}), 400

    new_payment = Payment(
        appointmentID=data['appointment_id'],
        paymentAmount=data['payment_amount'],
        status=False  
    )

    try:
        db.session.add(new_payment)
        db.session.commit()
        return jsonify({"payment_id": new_payment.paymentID, "status": new_payment.status}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/payment/<int:payment_id>", methods=['GET'])
def check_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    return jsonify({"payment_id": payment.paymentID, "success": payment.status}), 200


@app.route("/payment", methods=['PATCH'])
def update_payment():
    data = request.get_json()
    if not data or 'payment_id' not in data:
        return jsonify({"error": "Missing payment_id"}), 400

    payment = Payment.query.get(data['payment_id'])
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    payment.status = True  

    try:
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
@app.route("/payment/<int:payment_id>", methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    try:
        db.session.delete(payment)
        db.session.commit()
        return jsonify({"message": "Payment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
