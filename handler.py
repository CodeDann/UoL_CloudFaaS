import json
import requests
import pyodbc


def connect_to_db():

    cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:sc20jdpn-cw2-server.database.windows.net,1433;Database=sc20jdpn-cw2-db;Uid=user;Pwd={Password1};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    print(cursor.description)

def handle(req):
    # data = json.loads(req)
    # print("YOYO gotta connect to database")

    
    # print(data)
    connect_to_db()
 
# connect_to_db()