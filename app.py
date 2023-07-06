from flask import Flask, request, jsonify
from flask_mail import Mail

from app_config import set_config
from services.image_compression import compress_images
from services.email_gen import EmailInfo, generate_email

app = Flask(__name__)

set_config(app)
mail = Mail(app)


@app.route('/')
def hello_world():
    return "<p>Hello World</p>"


@app.route('/image_processing', methods=['POST'])
def process_images():
    uploaded_files = request.files.getlist('images')

    return jsonify({'compressed_images': compress_images(uploaded_files)})


@app.route('/email', methods=['POST'])
def send_email():
    email_info = EmailInfo(
        request.form.get('email_client'),
        request.form.get('channel'),
        request.form.get('type'),
        request.form.get('status'),
        request.form.get('description'),
        request.files.getlist('images')
    )
    message = generate_email(email_info)
    mail.send(message)
