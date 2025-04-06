from flask import Flask, request, redirect, render_template
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-checkout-session', methods=['GET','POST'])
#@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    # Hardcoded values for testing
    appointment_id = "AP12345"
    amount = 5000  # $50.00 in cents
    payment_id = "PAY98765"

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_intent_data={
                'metadata': {
                    'appointment_id': appointment_id,
                    'payment_id': payment_id
                }
            },
            line_items=[
                {
                    'price_data': {
                        'currency': 'sgd',
                        'unit_amount': amount,
                        'product_data': {
                            'name': f'Appointment {appointment_id}',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:5200/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5200/cancel',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e), 400

@app.route('/success')
def success():
    session_id = request.args.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
    
    # Here you would typically update your payment record
    # For now, we'll just return a success message with the payment details
    return f"Payment successful! Payment ID: {payment_intent.metadata.payment_id}, Amount: ${payment_intent.amount/100:.2f}, Appointment ID: {payment_intent.metadata.appointment_id}"

@app.route('/cancel')
def cancel():
    return "Payment cancelled. If you have any questions, please contact support."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)
