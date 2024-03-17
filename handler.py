import json
import requests


def handle(req):
    data = json.loads(req)
    print("YOYO gotta connect to database")
    print(data)
