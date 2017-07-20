# timestamp-age
This is a small flask app for getting the age of a timestamp from remote JSON specified by the URL of the JSON endpoint and the JSON path of the timestamp(s) to check. You can supply multiple JSON paths separated by commas to check at multiple paths.

It returns an object with the key-value pairs of the timestamp path and timestamp age.

# Usage
```shell
$ pip3 install -r requirements.txt
$ gunicorn --bind 0.0.0.0:${PORT} wsgi:app
$ curl -g http://localhost${PORT}/url=${JSON_URL}&path=${JSON_PATH}
```

Additional info:
+ Accepted timestamp formats: https://pendulum.eustace.io/docs/#parsing
+ JSON path tester: https://jsonpath.curiousconcept.com/
