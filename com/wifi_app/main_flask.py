from flask import Flask, request
import mysql.connector
import requests

connection = mysql.connector.connect(
        host="localhost",
        user="eshanjha",
        password="ILovebooks!@#123",
        database="wifi_db",
        port=3306
    )

app = Flask(__name__)

def remove_wifi(name, ssid):
    cursor = connection.cursor()

    if not name or not ssid:
        return {"status":"wrong fields"}, 400

    cursor.execute("DELETE FROM wifi_entries WHERE name = %s AND ssid = %s;", (name, ssid))
    connection.commit()
    return {"status":"removed"}, 200

@app.route("/new-wifi-entry", methods=["POST"])

def new_wifi_entry():
    cursor = connection.cursor()
    name = request.args.get("name")
    ssid = request.args.get("ssid")
    password = request.args.get("password")

    if not name or not ssid or not password:
        return {"status":"wrong fields"}, 400

    cursor.execute(
        "INSERT INTO wifi_entries VALUES (%s, %s, %s);",
        (name, ssid, password)
    )
    connection.commit()
    return {"status":200}

@app.route("/downvote", methods=["POST"])

def downvote():
    cursor = connection.cursor(dictionary=True)
    name = request.args.get("name")
    ssid = request.args.get("ssid")

    if not name or not ssid:
        return {"status":"wrong fields"}, 400

    downvotes_request = cursor.execute(
        "SELECT downvotes FROM wifi_entries WHERE name = %s AND ssid = %s;",
        (name, ssid)
        )
    downvotes = cursor.fetchone()[0]

    if downvotes == 6:
        remove_wifi(name, ssid)
        return {"status":"removed wifi"}, 200
    else:
        cursor.execute("UPDATE wifi_entries SET downvotes = downvotes + 1 WHERE name = %s AND ssid = %s;", (name, ssid))
        connection.commit()
        return {"status":"updated downvotes"}, 200







