import json
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from ds_recruitment_api import app


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    app.logger.error(json.dumps(payload))
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response
