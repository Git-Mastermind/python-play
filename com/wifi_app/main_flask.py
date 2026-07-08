from flask import Flask, request
import mysql.connector
import requests
from user_credentials import HOST, USER, PASSWORD, DATABASE

conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

app = Flask(__name__)

@app.route("/new-entry", methods = ["POST"])

def new_wifi_entry():
    cursor = conn.cursor()
    name = request.args.get("name")
    password = request.args.get("password")

    cursor.execute("INSERT INTO wifi_entries (name, password, downvotes) VALUES (%s, %s, %s);", (name, password, 0))
    