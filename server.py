#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
from crypt import methods
import os
import json
from flask import Flask, jsonify, redirect, render_template, request

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51L87ajJvldSQ1u1OL0Vh3Ypv3L3cvnsQfQ0wd45OQeWHe0OxeVFQ1yF6BLn8uJg20Zy1vArHWHM2unLJsACXHlkB0011PpnrW5'

app = Flask(__name__,template_folder='html', static_url_path='',static_folder='static')

YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_login_page')
def register():
    return render_template('register_login_page.html')

@app.route('/formando') 
def formandos():
    return render_template('formando.html')
    
@app.route('/formadores')
def formadores():
    return render_template('formadores.html')

@app.route('/form1')
def form1():
    return render_template('form1.html')

@app.route('/payments')
def payments():
    return render_template('payments.html')

@app.route('/conta')
def conta():
    return render_template('conta.html')
'''
def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='eur',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403
'''
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1L89FzJvldSQ1u1OczftrxrX',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url= YOUR_DOMAIN + '/success.html',
            cancel_url= YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


if __name__ == '__main__':
    app.run(port=4242)