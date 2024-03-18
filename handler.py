from mysql.connector import (connection)
import json

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

    try:
        cnx = connection.MySQLConnection(**config)
        cursor = cnx.cursor()
    except Exception as e:
        print("Error: ", e)
        return
    try:
        data = json.loads(req)
        city = get_val_or_error(data, "city")
    except ValueError as e:
        return str(e)
    


    # Execute the SELECT statement
    cursor.execute("SELECT * FROM averages")

    # Fetch all the rows
    rows = cursor.fetchall()

    for row in rows:
        print(row)

# handle("")