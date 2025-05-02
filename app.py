import os
from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
import re

app = Flask(__name__, static_folder="frontend")
CORS(app)

# Temporary storage for payment info
payment_data = {}

# Serve the frontend index.html at root path
@app.route('/api/paymentGateway')
def serve_gateway():
    return send_from_directory(os.path.join(app.root_path, 'frontend'), 'index.html')

# Save payment info and redirect to frontend
@app.route('/api/payment', methods=['POST'])
def save_payment_and_redirect():
    global payment_data
    data = request.get_json()

    amount = data.get('amount')
    item_name = data.get('itemName')

    if not amount or not item_name:
        return jsonify({"error": "Amount and orderItemName are required"}), 400

    payment_data = {
        "amount": amount,
        "itemName": item_name
    }

    # Redirect the user to frontend page
    return redirect(url_for('serve_gateway'))

# Provide payment info for frontend to prefill
@app.route('/api/payment-info', methods=['GET'])
def get_payment_info():
    global payment_data
    if payment_data:
        return jsonify(payment_data), 200
    else:
        return jsonify({"error": "No payment information available"}), 404

# Endpoint to process the actual payment
@app.route('/api/processPayment', methods=['POST'])
def process_payment():
    data = request.get_json()

    card_number = data.get('cardNumber')
    expiry_date = data.get('expiryDate')
    cvv = data.get('cvv')
    amount = data.get('amount')

    # Validation (same as before)
    if not card_number or not expiry_date or not cvv or not amount:
        return jsonify({"error": "All fields (card number, expiry date, CVV, and amount) are required"}), 400

    if not re.match(r"^\d{16}$", card_number):
        return jsonify({"error": "Invalid card number format. Must be 16 digits."}), 400

    if not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", expiry_date):
        return jsonify({"error": "Invalid expiry date format. Use MM/YY."}), 400

    if len(cvv) != 3 or not cvv.isdigit():
        return jsonify({"error": "Invalid CVV. It should be 3 digits."}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({"error": "Amount must be greater than zero."}), 400
    except ValueError:
        return jsonify({"error": "Invalid amount format."}), 400

    # Simulate random payment success/failure
    import random
    success = random.choice([True, False])

    if success:
        return jsonify({"success": True, "message": f"Payment of ${amount} processed successfully"}), 200
    else:
        return jsonify({"success": False, "message": "Payment failed. Please try again."}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
