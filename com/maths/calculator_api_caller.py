import requests

valid_operations = ["add", "subtract", "multiply", "divide"]
operation_input = input("add, subtract, multiply or divide? ")
operation_input = operation_input.lower()

while operation_input not in valid_operations:
    operation_input = input("add, subtract, multiply or divide? ")


num1 = int(input("Num1: "))
num2 = int(input("Num2: "))
url = f"http://127.0.0.1:5000/{operation_input}?num1={num1}&num2={num2}"

response = requests.get(url)
print(response.text)