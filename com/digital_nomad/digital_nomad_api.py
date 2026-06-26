from flask import Flask, jsonify, request
import mysql.connector
from credentials import HOST, USER, PASSWORD, DATABASE

connection = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

app = Flask(__name__)


@app.route("/get-venues", methods=["GET"])


def get_venues():
    cursor = connection.cursor()

    cursor.execute("SELECT name, address, wifi_password FROM venues;")
    venues_info = cursor.fetchall()
    return jsonify(venues_info)

@app.route("/new-venue", methods=["POST"])

def new_venue():
    cursor = connection.cursor()
    name = request.args.get()
    
    


if __name__=="__main__":
    app.run(debug=True)