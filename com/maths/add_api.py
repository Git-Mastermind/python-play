from flask import Flask, request

app = Flask(__name__)

@app.route("/add")

def add():
    return str(6 + 6)

if __name__ == "__main__":
    app.run(debug=True)