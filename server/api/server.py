import sys

from flask import Flask, request, jsonify

from flask_mongoengine import MongoEngine
from mongoengine import connect, MongoEngineConnectionError

from .api import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASS
from .models import User

DB = MongoEngine()

Routes = Blueprint('zindarak_server', __name__)


@Routes.route('/request_2fac', methods=['POST'])
def request_2fac():
    success = True
    status_code = 202
    try:
        json_req = request.get_json()
        if json_req is None:
            raise ValueError(
                'The JSON body could not be decoded ensure the Content-Type Header is set.'
            )
        username = json_req['username']
        user = User.get_user(username)
        devices = user.get_devices()
        for device in devices:
            device.set_auth_requested()
    except:
        success = False
        status_code = 500
    resp = jsonify({'success': success})
    resp.status_code = status_code
    return resp


def create_app() -> Flask:
    configs = [DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASS]
    if not any(configs):
        sys.exit('Atleast one DB Environment Variable is not set')

    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': DB_NAME,
        'host': DB_HOST,
        'port': DB_PORT,
        'username': DB_USER,
        'password': DB_PASS,
    }
    try:
        DB.init_app(app)
    except MongoEngineConnectionError as conn_err:
        print(conn_err)
        sys.exit('Could not connect to database.')

    app.register_blueprint(Routes)
    return app


def run_server():
    app = create_app()
    app.run()  # eventually put off debug
