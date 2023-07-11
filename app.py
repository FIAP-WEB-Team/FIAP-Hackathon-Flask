from flask import Flask, request, jsonify
from flask_mail import Mail

from app_config import set_config
from services.image_compression import compress_images
from services.email_gen import EmailInfo, Status, generate_email

app = Flask(__name__)

set_config(app)
mail = Mail(app)


@app.route('/')
def hello_world():
    return "<p>Hello FIAPers</p>"


@app.route('/image_processing', methods=['POST'])
def process_images():
    uploaded_files = request.files.getlist('images')

    return jsonify({'compressed_images': compress_images(uploaded_files)})


@app.route('/email', methods=['POST'])
def send_email():
    email_info = EmailInfo(
        request.json.get('ticket_id'),
        request.json.get('client_name'),
        request.json.get('email_client'),
        request.json.get('channel'),
        request.json.get('type'),
        request.json.get('level'),
        Status[request.json.get('status').upper()],
        request.json.get('description'),
        request.json.get('images'),
        request.json.get('clerk_description')
    )
    message = generate_email(email_info)
    mail.send(message)
    
    return {}
