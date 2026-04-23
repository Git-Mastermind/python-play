from flask import Flask, request

app = Flask(__name__)



@app.route("/add")

def add():
    num1 = request.args.get("num1", 0)
    num2 = request.args.get("num2", 0)
    num1 = int(num1)
    num2 = int(num2)
    return str(num1 + num2)

@app.route("/subtract")

def subtract():
    num1 = request.args.get("num1")
    num1 = int(num1)

    num2 = request.args.get("num2")
    num2 = int(num2)

    return str(num1 - num2)

@app.route("/multiply")

def multiply():
    num1 = request.args.get("num1")
    num1 = int(num1)
    
    num2 = request.args.get("num2")
    num2 = int(num2)

    return str(num1 * num2)

@app.route("/divide")

def divide():
    num1 = request.args.get("num1")
    num1 = int(num1)

    num2 = request.args.get("num2")
    num2 = int(num2)

    return str(num1 / num2)

if __name__ == "__main__":
    app.run(debug=True)