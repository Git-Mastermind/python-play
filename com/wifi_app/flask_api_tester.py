import requests

name = input("Name:")
password = input("Password: ")

url = f"http://127.0.0.1:5000/new-entry?name={name}&password={password}"
requests.post(url)