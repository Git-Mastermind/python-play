from flask import Flask, request, jsonify
import requests
import pymysql
from pymysql.cursors import DictCursor
import os
from user_credentials import *


conn = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE,
    port=PORT
)
# Run this once to build the table on your new cloud database
with conn.cursor() as setup_cursor:
    setup_cursor.execute("""
    CREATE TABLE IF NOT EXISTS wifi_entries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        password VARCHAR(255),
        downvotes INT DEFAULT 0
    );
    """)
    conn.commit()

app = Flask(__name__)

@app.route("/new-entry", methods = ["POST"])

def new_wifi_entry():
    cursor = conn.cursor()
    name = request.args.get("name")
    password = request.args.get("password")

    cursor.execute("INSERT INTO wifi_entries (name, password, downvotes) VALUES (%s, %s, %s);", (name, password, 0))
    conn.commit()
    cursor.close()

    return {"status":"created"}, 201



@app.route("/get-wifis", methods=["GET"])

def get_wifis():
    cursor = conn.cursor(DictCursor)

    cursor.execute("SELECT * FROM wifi_entries;")
    wifis_response = cursor.fetchall()
    cursor.close()
    return jsonify(wifis_response), 200

@app.route("/downvote", methods=["POST"])

def downvote():
    cursor = conn.cursor(DictCursor)
    id = request.args.get("id")

    cursor.execute("SELECT downvotes FROM wifi_entries WHERE id = %s;", (id))
    wifi = cursor.fetchall()
    if not wifi:
        return {"status":"invalid name or id"}, 400
    downvotes = cursor.fetchall()[0]["downvotes"]
    if downvotes >= 5:
        cursor.execute("DELETE FROM wifi_entries WHERE id = %s;", (id))
        conn.commit()
        return {"status":"wifi deleted"}, 204
     
    cursor.execute("UPDATE wifi_entries SET downvotes = downvotes + 1 WHERE id = %s;", (id))
    conn.commit()
    cursor.close()

    return {"status":"updated downvotes"}, 200

@app.route("/search", methods=["GET"])

def search():
    cursor = conn.cursor(DictCursor)
    name = request.args.get("name")

    cursor.execute("SELECT * FROM wifi_entries WHERE name = %s;", (name))
    wifi_response = cursor.fetchall()
    if not wifi_response:
        return {"status":"no wifis available"}, 400
    return wifi_response, 200

@app.route("/is-in", methods=["GET"])

def is_in():
    cursor = conn.cursor(DictCursor)
    name = request.args.get("name")

    cursor.execute("SELECT id FROM wifi_entries WHERE name = %s;", (name))
    returned_id = cursor.fetchall()
    if not returned_id:
        return {"status":"wifi passed is invalid"}, 400
    else:
        return {"status":"wifi passed is valid"}, 200


if __name__ == "__main__":
    app.run(debug=True)
