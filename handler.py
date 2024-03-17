import json
import requests


def get_val_or_error(request, key):
    val = request.get(key)
    if val is None or val == "":
        raise ValueError(f"Missing required parameter '{key}'")


def handle(req):
    try:
        data = json.loads(req)
        latitude = get_val_or_error(data, 'lat')
        longitude = get_val_or_error(data, 'long')
    except ValueError as e:
        print(str(e))
    except Exception as e:
        print(str(e))

    # # todo store API more securely
    api_key = "044d96d0a9150903ca5e80fc1a5da8e7"

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
        response = requests.get(url)
        data = response.json()    
        print(json.dumps(data))
    except Exception as e:
        print(str(e))