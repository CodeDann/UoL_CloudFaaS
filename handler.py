import json
import requests
import pyodbc

# import mysql.connector

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
        cnx.close()
        print("connected")
    except Exception as e:
        print("Error: ", e)

def handle(req):
    connect_to_db()
 
# connect_to_db()
# handle("")