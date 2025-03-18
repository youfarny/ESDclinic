import os
import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)
CORS(app)  # Enable CORS

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# ✅ API: Create a Stripe Checkout Session
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        data = request.get_json()
        session = stripe.checkout.Session.create(
            payment_method_types=["card", "apple_pay", "google_pay"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Premium Service"},
                        "unit_amount": int(data["amount"]) * 100,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
        )
        return jsonify({"id": session.id})
    except Exception as e:
        return jsonify(error=str(e)), 500

# ✅ API: Webhook for Payment Confirmation
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

        if event["type"] == "checkout.session.completed":
            print("✅ Payment Successful!", event["data"]["object"])

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200, debug=True)
