# -*- coding: utf-8 -*-
"""\
Flask app fro QRCards UI
"""
import io
import base64
import json
from flask import Flask, render_template, request, send_file, abort
import segno

app = Flask(__name__)

@app.route('/')
def home():
  first_name = request.args.get('first_name')
  last_name = request.args.get('last_name')
  email = request.args.get('email')
  phone = request.args.get('phone')

  data = {
    'first_name': first_name,
    'last_name': last_name,
    'email': email,
    'phone': phone
  }

  base64_data = base64.b64encode(json.dumps(data).encode('utf-8'))

  return render_template('index.html', data=base64_data)

@app.route('/qr/' , methods = ['GET', 'POST'])
def qrcode_svg():
  base64_data = request.args.get('data')
  data = json.loads(base64.b64decode(base64_data))

  first_name = data.get('first_name')
  last_name = data.get('last_name')
  email = data.get('email')
  phone = data.get('phone')

  buff = io.BytesIO()
  qrcode = segno.helpers.make_mecard(name=f'{last_name},{first_name}', email=email, phone=phone)
  qrcode.save(buff, kind='svg', scale=4)
  buff.seek(0)

  return send_file(buff, mimetype='image/svg+xml')

def web():
  app.run(debug=True, port=5673)

if __name__ == '__main__':
  web()
