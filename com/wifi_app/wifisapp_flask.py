from flask import Flask, request, jsonify
import mysql.connector
import requests

def connect_database():
     return mysql.connector.connect(
            host="localhost",
            user="eshanjha",
            password="ILovebooks!@#123",
            database="wifi_db",
            port=3306
        )

app = Flask(__name__)

def remove_wifi(name, ssid):
    connection = connect_database()
    cursor = connection.cursor()

    if not name or not ssid:
        return {"status":"wrong fields"}, 400

    cursor.execute("DELETE FROM wifi_entries WHERE name = %s AND ssid = %s;", (name, ssid))
    connection.commit()
    return {"status":"removed"}, 200

@app.route("/get-all-wifis", methods=["GET"])

def get_all_wifis():
    connection = connect_database()
    cursor = connection.cursor(dictionary=True)
    

    wifis_data_dict = cursor.execute("SELECT name, ssid, password, downvotes FROM wifi_entries")
    names = wifis_data_dict["name"]
    ssids = wifis_data_dict["ssid"]
    downvotes = wifis_data_dict["downvotes"]
    return names, ssids, downvotes

@app.route("/new-wifi-entry", methods=["POST"])

def new_wifi_entry():
    connection = connect_database()
    cursor = connection.cursor()
    name = request.args.get("name")
    ssid = request.args.get("ssid")
    password = request.args.get("password")

    if not name or not ssid or not password:
        return {"status":"wrong fields"}, 400

    try:
        cursor.execute(
            "INSERT INTO wifi_entries (name, ssid, password, downvotes) VALUES (%s, %s, %s, %s);",
            (name, ssid, password, 0)
        )
        connection.commit()
        return {"status":"created"}, 201
    except mysql.connector.Error:
        return {"status" : "internal database error"}, 503

@app.route("/downvote", methods=["POST"])

def downvote():
    connection = connect_database()
    cursor = connection.cursor(dictionary=True)
    name = request.args.get("name")
    ssid = request.args.get("ssid")

    if not name or not ssid:
        return {"status":"wrong fields"}, 400

    cursor.execute("SELECT downvotes FROM wifi_entries WHERE name = %s AND ssid = %s;", (name, ssid))
    downvote_row = cursor.fetchone()
    downvotes = downvote_row["downvotes"]


    if downvotes >= 6:
        remove_wifi(name, ssid)
        print(cursor.rowcount)
        return {"status":"removed wifi"}, 200
    else:
        cursor.execute("UPDATE wifi_entries SET downvotes = downvotes + 1 WHERE name = %s AND ssid = %s;", (name, ssid))
        connection.commit()
        print(cursor.rowcount)
        return {"status":"updated downvotes"}, 200
    
@app.route("/get-ssid", methods=["GET"])

def get_ssid():
    connection = connect_database()
    cursor = connection.cursor(dictionary=True)
    name = request.args.get("name")

    cursor.execute("SELECT ssid FROM wifi_entries WHERE name = %s;", (name,))
    row_ssid = cursor.fetchone()
    if not row_ssid:
        return {"status":"no ssid found"}, 404
    ssid = row_ssid["ssid"]
    
    return {
        "status" : ssid
    }

    
    

if __name__ == "__main__":
    app.run(debug=True)







