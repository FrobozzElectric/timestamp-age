from flask import abort, Flask, jsonify, make_response, request
from jsonpath_rw import parse
import json
import pendulum
import requests

app = Flask(__name__)


def calculate_age(timestamp):
    now = pendulum.now()
    try:
        timestamp_parsed = pendulum.parse(timestamp)
    except:
        return 'unable to parse timestamp'
    age = now.diff(timestamp_parsed).in_seconds()
    return age


def parse_json(data, path):
    try:
        jsonpath_expr = parse(path)
    except:
        return {path: 'invalid JSON path'}
    matches = {}
    for match in jsonpath_expr.find(data):
        matches[str(match.full_path)] = calculate_age(match.value)
    return matches


def abort_request(message, status):
    abort(make_response(jsonify(error=message, code=status), status))


@app.route('/_healthcheck')
def healthcheck():
    return jsonify({'status': 'ok'})


@app.route('/')
def timestamp_age():
    args = request.args
    if 'url' in args and 'path' in args:
        url = args.get('url')
        paths = args.get('path').split(',')
    else:
        abort_request('missing \'url\' or \'path\' parameter', 422)
    try:
        r = requests.get(url)
        r.raise_for_status()
    except Exception as error:
        code = r.status_code if 'r' in vars() else 500
        abort_request(str(error), code)
    try:
        data = json.loads(r.text)
    except ValueError:
        abort_request('invalid JSON', 422)
    results = {'code': 200, 'error': None}
    for path in paths:
        results.update(parse_json(data, path))
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
