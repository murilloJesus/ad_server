from flask import request
from app.models.activity_directory_model import ADModel
from app.views.response_view import success_response, error_response
from config.ad_server import Config

ad_model = ADModel(Config.AD_SERVER, Config.AD_DOMAIN)

def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return error_response('Usuário e senha são necessários', 400)

    auth_result = ad_model.authenticate(username, password)
    if auth_result:
        return success_response(auth_result, 200)
    else:
        return error_response('Credenciais inválidas', 401)