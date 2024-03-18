import json
import requests
from mysql.connector import (connection)

config = {
  'user': 'jaken',
  'password': 'i_love_cloud1',
  'host': 'sc20jdpn-mysql-db.mysql.database.azure.com',
  'database': 'data',
  'raise_on_warnings': True,
}

def get_val_or_error(request, key):
    val = request.get(key)
    if val is None or val == "":
        raise ValueError(f"Missing required parameter '{key}'")
    return val


def handle(req):
    # connect to the database
    try:
        cnx = connection.MySQLConnection(**config)
        cursor = cnx.cursor()
    except Exception as e:
        return {
            "status": 500,
            "message": "Failed to connect to the database"
        }
    # parse the request
    try:
        req = json.loads(req)
        city = get_val_or_error(req, "city")
        wind = get_val_or_error(req, "wind")
        temp = get_val_or_error(req, "temp")
        max_temp = get_val_or_error(req, "temp_min")
        min_temp = get_val_or_error(req, "temp_max")
        humidity = get_val_or_error(req, "humidity")
        pressure = get_val_or_error(req, "pressure")
    except Exception as e:
        return {
            "status": 400,
            "message": str(e)
        }


    # get max vals from db
    try:
        query = ("SELECT * FROM red_flags WHERE city_name = %s")
        cursor.execute(query, (city,))
        row = cursor.fetchone()
        if row is not None:
            max_wind = row[1]
            max_temp = row[2]
            max_humidity = row[3]
            max_pressure = row[4]
        else:
            raise ValueError(f"City '{city}' not found in database")
    except Exception as e:
        return {
            "status": 500,
            "message": "Failed to get max vals from db" + str(e)
        }
    
    # check if any vals are above the max
    returnMsg = ""
    errorFlag = False
    if float(wind) > max_wind:
        returnMsg += "Warning: Wind is too high\n"
        errorFlag = True
    if float(temp) > max_temp:
        returnMsg += "Warning: Temperature is too high\n"
        errorFlag = True
    if float(humidity) > max_humidity:
        returnMsg += "Warning: Humidity is too high\n"
        errorFlag = True
    if float(pressure) > max_pressure:
        returnMsg += "Warning: Pressure is too high\n"
        errorFlag = True
    
    if errorFlag == False:
        returnMsg = "All values are within the acceptable range\n"

    return {
        "status": 200,
        "message": returnMsg,
    }

# print(handle({
#     "city": "London",
#     "wind": 3,
#     "temp": 20,
#     "max_temp": 25,
#     "min_temp": 15,
#     "humidity": 50,
#     "pressure": 1010
# }))