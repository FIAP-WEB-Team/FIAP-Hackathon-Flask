import os
import yaml
from flask import Flask


CREDENTIALS_FILE = '/credentials/gmail_secret.yaml'


def _load_email_config():
    base_path = os.path.dirname(os.path.abspath(__file__))
    with open(base_path + CREDENTIALS_FILE, 'r', encoding='UTF-8') as file:
        credentials = yaml.safe_load(file)['default']
    return credentials['username'], credentials['password']


def set_config(app: Flask):
    username, password = _load_email_config()
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = username
    app.config['MAIL_PASSWORD'] = password
    app.config['MAIL_DEFAULT_SENDER'] = username
