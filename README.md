# timestamp-age
This is a small flask app for getting the age of a timestamp from JSON specficed by the path of the JSON endpoint and the JSON path of the timestamp(s) to check.

It returns an object with the key-value pairs of the timestamp path and timestamp age.

# Usage
```shell
$ pip3 install -r requirements.txt
$ gunicorn --bind 0.0.0.0:${PORT} wsgi:app
$ curl http://localhost${PORT}/url=${JSON_URL}&path=${JSON_PATH}
```
