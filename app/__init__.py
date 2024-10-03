from flask import Flask
from app.controllers import login

def create_app():
    app = Flask(__name__)

    # Rota de autenticação
    app.add_url_rule('/login', view_func=login, methods=['POST'])

    return app