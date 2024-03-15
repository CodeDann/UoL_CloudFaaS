import json
import requests


def get_val_or_error(request, key):
    json_req = json.loads(request)
    r = requests.get(json_req[f"{key}"])
    if r is None or r.text == "":
        raise ValueError(f"Missing required parameter '{key}'")


def handle(req):
    try:
        latitude = get_val_or_error(req, 'lat')
        longitude = get_val_or_error(req, 'long')
    except ValueError as e:
        print(str(e))
        # return func.HttpResponse(str(e), status_code=400)

    # todo store API more securely
    api_key = "044d96d0a9150903ca5e80fc1a5da8e7"

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(str(e))
        # return func.HttpResponse(str(e), status_code=500)

    print(json.dumps(data))
    # return func.HttpResponse(json.dumps(data), status_code=200)