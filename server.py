#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""

from cgitb import lookup
import os
import json
from unittest import result
from flask import Flask, jsonify, redirect, render_template, request

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51L87ajJvldSQ1u1OL0Vh3Ypv3L3cvnsQfQ0wd45OQeWHe0OxeVFQ1yF6BLn8uJg20Zy1vArHWHM2unLJsACXHlkB0011PpnrW5'

app = Flask(__name__,template_folder='html', static_url_path='', static_folder='static')

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

@app.route('/plans')
def plans():

    return render_template('payments.html')


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        print("Trying prices")
        prices = stripe.Price.list(
            product=request.form.get('product'),
            active='true'
            )
        for i in range(2):
            if prices.data[i].recurring.interval == request.form.get('nickname'):
                final = prices.data[i]
            else:
                final = prices.data[0]
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': final.id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN +
            '/success.html?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e :
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242)