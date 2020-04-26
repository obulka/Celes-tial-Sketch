import base64
import json
from random import uniform

from flask import Flask, request


def generate_star_map(num_stars):
    """
    """
    return [(uniform(0, 360), uniform(0, 180)) for _ in range(num_stars)]


def create_new_character(request_data):
    num_stars = request_data.get('num_stars')

    if not num_stars:
        return json.dumps({'success': False, 'failureInfo': 'Request data missing'}), 400

    resp = {"star_map": generate_star_map(num_stars)}
    if not resp.get('data'):
        return json.dumps({'success': False, 'failureInfo': 'Error in star map creation'}), 418

    encoded_data = base64.b64encode(resp['data'].encode('utf-8')).decode('utf-8')

    return json.dumps({'success': True, 'data': encoded_data})
