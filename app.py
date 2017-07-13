from flask import Flask, jsonify, request
from jsonpath_rw import parse
import json
import pendulum
import requests

app = Flask(__name__)

def calculate_age(timestamp):
    now = pendulum.now()
    try:
        timestamp_parsed = pendulum.parse(timestamp)
    except Exception as error:
        return str(error)
    age = now.diff(timestamp_parsed).in_seconds()
    return age

def parse_json(data, path):
    try:
        jsonpath_expr = parse(path)
    except Exception as error:
        return {path: str(error)}
    matches = {}
    for match in jsonpath_expr.find(data):
        matches[str(match.full_path)] = calculate_age(match.value)
    return matches

@app.route('/_healthcheck')
def healthcheck():
    return jsonify({'status': 'ok'})

@app.route('/')
def timestamp_age():
    args = request.args
    if 'url' in args and 'path' in args:
        url = args.get('url')
        paths = args.get('path').split(",")
    else:
        return jsonify({'error': 'missing "url" or "path" parameter'}), 422
    try:
        r = requests.get(url)
        r.raise_for_status()
    except Exception as error:
        return jsonify({'error': str(error)}), 500
    data = json.loads(r.text)
    results = {}
    for path in paths:
        results.update(parse_json(data, path))
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
