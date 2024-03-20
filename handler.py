from mysql.connector import (connection)
import json
import pandas as pd
import datetime

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
    
    # save data to database
    try:
        cursor.execute("INSERT INTO weather (city_name, wind, temp, max_temp, min_temp, humidity, pressure) VALUES (%s, %s, %s, %s, %s, %s, %s)", (city, wind, temp, max_temp, min_temp, humidity, pressure))
        cnx.commit()
    except Exception as e:
        return {
            "status": 500,
            "message": "Failed to save data to the database" + str(e)
        }
    
    # calcualte averages for this city
    try:
        cursor.execute("SELECT wind, temp, humidity, pressure FROM weather WHERE city_name = %s", (city,))
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["wind", "temp", "humidity", "pressure"])
        # calculate averages
        averages = df.mean()
        # calculate the standard deviation
        std_dev = df.std()
        # check if city already exists in the database
        cursor.execute("SELECT city_name FROM stats WHERE city_name = %s", (city,))
        if cursor.fetchone() is None:
            # insert new city to the database
            cursor.execute("INSERT INTO stats (city_name, average_temp, deviation_temp, average_wind, deviation_wind, average_humidity, deviation_humidity, average_pressure, deviation_pressure, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (city, float(averages["temp"]), float(std_dev["temp"]), float(averages["wind"]), float(std_dev["wind"]), float(averages["humidity"]), float(std_dev["humidity"]), float(averages["pressure"]), float(std_dev["pressure"]), datetime.datetime.now())
            cnx.commit()
        else:
            # update means and standard deviation to the database
            cursor.execute("""
                UPDATE stats 
                SET average_temp = %s, 
                    deviation_temp = %s, 
                    average_wind = %s, 
                    deviation_wind = %s, 
                    average_humidity = %s, 
                    deviation_humidity = %s, 
                    average_pressure = %s, 
                    deviation_pressure = %s
                WHERE city_name = %s
            """, (float(averages["temp"]), float(std_dev["temp"]), float(averages["wind"]), float(std_dev["wind"]), float(averages["humidity"]), float(std_dev["humidity"]), float(averages["pressure"]), float(std_dev["pressure"]), city))
            cnx.commit()
    except Exception as e:
        return {
            "status": 500,
            "message": "Failed to calculate averages" + str(e)
        }
    

    # close the connection
    cursor.close()
    cnx.close()
    return {
        "status": 200,
        "message": "Data saved successfully"
    }


# print(handle(json.dumps({
#     "city": "London",
#     "wind": 1,
#     "temp": 20,
#     "temp_max": 25,
#     "temp_min": 15,
#     "humidity": 50,
#     "pressure": 1010
# })))