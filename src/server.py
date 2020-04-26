import webservices

from flask import Flask, json, request

import base64
import mysql.connector

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]


api = Flask(__name__)


sql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="database_name"
)

def _request_data(request):
    if not request.data:
        return None

    decoded = request.data.decode()
    loaded_data = json.loads(decoded)
    print(f"Loaded: {loaded_data}")
    return loaded_data

def _request_form(request):
    if not request.form:
        return None

    loaded_data = request.form.to_dict()
    return loaded_data


@api.route('/star_map/new', methods=['GET'])
def get_star_map():
    request_data = _request_form(request)
    if not request_data:
        return {'success': False, 'failureInfo': 'No request data'}, 400

    resp = webservices.create_star_map(request_data)
    return resp



@api.route('/healthcheck', methods=['GET'])
def ws_health_check():
    return json.dumps({'status': 200})



@api.route('/')
def hello_world():
        return 'Hello, World!'

@api.route('/companies', methods=['GET'])
def get_companies():
    return json.dumps(companies)

@api.route('/companies', methods=['POST'])
def post_companies():
    return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run()
