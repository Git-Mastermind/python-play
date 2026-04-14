import requests

num1 = int(input("Num1: "))
num2 = int(input("Num2: "))
url = f"http://127.0.0.1:5000/add?num1={num1}&num2={num2}"

response = requests.get(url)
print(response.json())