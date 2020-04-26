from citrus import webservices

from flask import Flask, json, request

import base64


api = Flask(__name__)

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


@api.route('/starmap/new', methods=['POST'])
def update_star_map():
    request_data = _request_form(request)
    if not request_data:
        return {'success': False, 'failureInfo': 'Invalid request data'}, 400

    return webservices.create_star_map(request_data)


@api.route('/healthcheck', methods=['GET'])
def ws_health_check():
    return json.dumps({'status': 200})


if __name__ == '__main__':
    api.run()
