import json
import requests


def get_val_or_error(request, key):
    val = request.get(key)
    if val is None or val == "":
        raise ValueError(f"Missing required parameter '{key}'")


def handle(req):
    try:
        latitude = get_val_or_error(req, 'lat')
        longitude = get_val_or_error(req, 'long')
    except ValueError as e:
        return str(e)
        # print(str(e))
        # return func.HttpResponse(str(e), status_code=400)
    print(latitude, longitude)
    # todo store API more securely
    api_key = "044d96d0a9150903ca5e80fc1a5da8e7"

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
        response = requests.get(url)
        data = response.json()    
        print(json.dumps(data))
    except Exception as e:
        print(str(e))
        # return func.HttpResponse(str(e), status_code=500)

    # return func.HttpResponse(json.dumps(data), status_code=200)
        
    


# def handle(req):
#     print(req)
    # result = {"result": ""}

    # json_req = json.loads(req)

    # lat = requests.get(json_req["lat"])
    # if json_req["lat"] not in lat.text:
    #     result = {"result": "Error: latitude not found in request"}

    # long = requests.get(json_req["long"])
    # if json_req["long"] not in long.text:
    #     result = {"result": "Error: longitude not found in request"}

    # api_key = "044d96d0a9150903ca5e80fc1a5da8e7"


    # if result["result"] == "":
    #     try:
    #         url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}"
    #         response = requests.get(url)
    #         data = response.json()
    #         result = {"result": data}    
    #     except Exception as e:
    #         result = {"result": str(e)}
    
    # print(json.dumps(result))






# print(handle('{"lat": 51.5074, "long": 0.1278}')
