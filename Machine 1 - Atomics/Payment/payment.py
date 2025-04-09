from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from dotenv import load_dotenv
from flask_cors import CORS

import os
import stripe


app = Flask(__name__)
CORS(app, origins=["*"])

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ESD213password!@116.15.73.191:3306/payment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Swagger
swagger = Swagger(app)

class Payment(db.Model):
    __tablename__ = 'payment'
    
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.Boolean, default=False)  # False means not paid, True means paid
    payment_amount = db.Column(db.Float, nullable=False)
    insurance = db.Column(db.Boolean, default=False)

    def json(self):
        return {
            "payment_id": self.payment_id,
            "appointment_id": self.appointment_id,
            "payment_status": self.payment_status,
            "payment_amount": self.payment_amount,
            "insurance": self.insurance
        }

with app.app_context():
    db.create_all()


@app.route("/payment", methods=['POST'])
def create_payment():
    """
    Create a new payment record
    ---
    tags:
      - Payment
    parameters:
      - name: body
        in: body
        required: true
        description: Payment data to create a new payment
        schema:
          type: object
          properties:
            appointment_id:
              type: integer
            payment_amount:
              type: number
              format: float
            insurance:  
              type: boolean
    responses:
      201:
        description: Payment successfully created
        schema:
          type: object
          properties:
            payment_id:
              type: integer
            payment_status:
              type: boolean
      400:
        description: Missing appointment_id,payment_amount or insurance
    """
    data = request.get_json()
    if not data or 'appointment_id' not in data or 'payment_amount' not in data or 'insurance' not in data:
        return jsonify({"error": "Missing appointment_id, payment_amount or insurance"}), 400

    new_payment = Payment(
        appointment_id=data['appointment_id'],
        payment_amount=data['payment_amount'],
        insurance=data['insurance'],
        payment_status=False  
    )

    try:
        db.session.add(new_payment)
        db.session.commit()
        return jsonify({"payment_id": new_payment.payment_id, "payment_status": new_payment.payment_status}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/payment/<int:payment_id>", methods=['GET'])
def check_payment(payment_id):
    """
    Check payment payment_status
    ---
    tags:
      - Payment
    parameters:
      - name: payment_id
        in: path
        required: true
        description: The payment ID to check payment_status
        type: integer
    responses:
      200:
        description: Payment found with its payment_status
        schema:
          type: object
          properties:
            payment_id:
              type: integer
            success:
              type: boolean
      404:
        description: Payment not found
    """
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    return jsonify({"payment_id": payment.payment_id, "success": payment.payment_status}), 200


@app.route("/payment", methods=['PATCH'])
def update_payment():
    """
    Update payment payment_status to 'paid'
    ---
    tags:
      - Payment
    parameters:
      - name: body
        in: body
        required: true
        description: Payment ID to mark as paid
        schema:
          type: object
          properties:
            payment_id:
              type: integer
    responses:
      200:
        description: Payment successfully updated to 'paid'
      400:
        description: Missing payment_id
      404:
        description: Payment not found
    """
    data = request.get_json()
    if not data or 'payment_id' not in data:
        return jsonify({"error": "Missing payment_id"}), 400

    payment = Payment.query.get(data['payment_id'])
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    payment.payment_status = True  

    try:
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/payment/<int:payment_id>", methods=['DELETE'])
def delete_payment(payment_id):
    """
    Delete a payment record
    ---
    tags:
      - Payment
    parameters:
      - name: payment_id
        in: path
        required: true
        description: The payment ID to delete
        type: integer
    responses:
      200:
        description: Payment deleted successfully
      404:
        description: Payment not found
    """
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    try:
        db.session.delete(payment)
        db.session.commit()
        return jsonify({"message": "Payment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


load_dotenv()  # this loads from .env
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route("/payment/verify", methods=['POST'])
def verify_stripe_payment():
    """
    Verify Stripe session and mark payment as paid
    ---
    tags:
      - Payment
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            appointment_id:
              type: integer
            session_id:
              type: string
    responses:
      200:
        description: Payment verified and updated
      400:
        description: Invalid session or payment not found
      500:
        description: Stripe or DB error
    """
    data = request.get_json()
    appointment_id = data.get("appointment_id")
    session_id = data.get("session_id")

    if not appointment_id or not session_id:
        return jsonify({"error": "Missing appointment_id or session_id"}), 400

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        if session['payment_status'] != 'paid':
            return jsonify({"error": "Payment not completed"}), 400

        # Find the payment record
        payment = Payment.query.filter_by(appointment_id=appointment_id).first()
        if not payment:
            return jsonify({"error": "Payment record not found for this appointment"}), 404

        payment.payment_status = True
        db.session.commit()

        return jsonify({"message": "Payment verified and marked as paid"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/payment/appointment/<int:appointment_id>', methods=['GET'])
def get_payment_by_appointment(appointment_id):
    """
    Retrieve payment info for a given appointment_id
    ---
    tags:
      - Payment
    parameters:
      - name: appointment_id
        in: path
        required: true
        description: The appointment ID to get payment details for
        type: integer
    responses:
      200:
        description: Payment data retrieved
        schema:
          type: object
          properties:
            payment_id:
              type: integer
            appointment_id:
              type: integer
            payment_amount:
              type: number
              format: float
            payment_status:
              type: boolean
      404:
        description: Payment record not found
    """
    payment = Payment.query.filter_by(appointment_id=appointment_id).first()
    if not payment:
        return jsonify({"error": "Payment record not found"}), 404
    return jsonify(payment.json()), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5105)
