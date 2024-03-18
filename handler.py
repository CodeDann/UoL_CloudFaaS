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
        print("Error: ", e)
        return

    try:
        data = json.loads(req)
        if len(data) == 0:
            raise ValueError("No data provided")
        elif len(data) == 1:
            city = get_val_or_error(data, "city")
            coords = get_coords_from_db(cursor, city)
        elif len(data) == 3:
            city = get_val_or_error(data, "city")
            latitude = get_val_or_error(data, "lat")
            longitude = get_val_or_error(data, "lon")
            # check if the city exists in the database
            coords = get_coords_from_db(cursor, city)
            if coords is None:
                # if not, add it
                add_city_to_db(cursor, cnx, city, latitude, longitude)
            else:
                # if it does, update the coordinates
                update_city_in_db(cursor, cnx, city, latitude, longitude)
    except ValueError as e:
        print(str(e))
        return

    if coords is not None:
        call_api(coords[0], coords[1])
    else:
        print(f"City '{city}' not found in the database\n If you want to add it to the database, please provide the latitude and longitude.")
   

def get_coords_from_db(cursor, city):
    try:
        query = f"SELECT latitude, longitude FROM cities WHERE city_name = '{city}'"
        cursor.execute(query)
        row = cursor.fetchone()
        if row is not None:
            latitude = row[0]
            longitude = row[1]
            return [latitude, longitude]
        else:
            return None
    except Exception as e:
        print(str(e))

def call_api(latitude, longitude):
    api_key = "044d96d0a9150903ca5e80fc1a5da8e7"

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
        response = requests.get(url)
        data = response.json()    
        print(json.dumps(data))
    except Exception as e:
        print(str(e))


def add_city_to_db(cursor, cnx, city, latitude, longitude):
    try:
        query = f"INSERT INTO cities (city_name, latitude, longitude) VALUES ('{city}', {latitude}, {longitude})"
        cursor.execute(query)
        print(f"Added city '{city}' to the database")
        cnx.commit()
    except Exception as e:
        print(str(e))

def update_city_in_db(cursor, cnx, city, latitude, longitude):
    try:
        query = f"UPDATE cities SET latitude = {latitude}, longitude = {longitude} WHERE city_name = '{city}'"
        cursor.execute(query)
        print(f"Updated city '{city}' in the database")
        cnx.commit()
    except Exception as e:
        print(str(e))

# handle('{"city": "BRUM"}')