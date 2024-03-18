from mysql.connector import (connection)

config = {
  'user': 'jaken',
  'password': 'i_love_cloud1',
  'host': 'sc20jdpn-mysql-db.mysql.database.azure.com',
  'database': 'data',
  'raise_on_warnings': True,

}

def connect_to_db():
    try:
        cnx = connection.MySQLConnection(**config)
        cursor = cnx.cursor()
        return cursor
    except Exception as e:
        print("Error: ", e)

def handle(req):
    cursor = connect_to_db()
    # Execute the SELECT statement
    cursor.execute("SELECT * FROM averages")

    # Fetch all the rows
    rows = cursor.fetchall()

    for row in rows:
        print(row)
