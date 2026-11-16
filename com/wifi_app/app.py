import re
from better_profanity import profanity
from flask_cors import CORS
from flask import Flask, request, jsonify
import pymysql
from pymysql.cursors import DictCursor
import os

if os.environ.get("HOST"):
    HOST = os.environ.get("HOST")
    USER = os.environ.get("USER")
    PASSWORD = os.environ.get("PASSWORD")
    DATABASE = os.environ.get("DATABASE")
else:
    from user_credentials import HOST, USER, PASSWORD, DATABASE

def get_db():
    return pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        cursorclass=DictCursor
    )

# Initialize table on startup
init_conn = get_db()
try:
    with init_conn.cursor() as setup_cursor:
        setup_cursor.execute("""
        CREATE TABLE IF NOT EXISTS wifi_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            password VARCHAR(255),
            downvotes INT NOT NULL DEFAULT 0,
            upvotes INT NOT NULL DEFAULT 0
        );
        """)
        init_conn.commit()
finally:
    init_conn.close()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://opensignal-wifi.vercel.app"]}})

profanity.load_censor_words()
BLOCKED_TERMS = {"goon", "gooning", "skibidi", "gyatt", "rizz", "diddy", "spam", "stupid", "idiot", "dumb"}

def is_clean_text(text):
    if not text or len(text) > 64:
        return False
    lowered = text.lower()
    if profanity.contains_profanity(lowered):
        return False
    words = set(re.findall(r"[a-z0-9]+", lowered))
    if words & BLOCKED_TERMS:
        return False
    return bool(re.match(r"^[\x20-\x7E]+$", text))

@app.route("/new-entry", methods=["POST"])
def new_wifi_entry():
    name = (request.args.get("name") or "").strip()
    password = (request.args.get("password") or "").strip()

    if not is_clean_text(name):
        return jsonify({"status": "Invalid or disallowed network name"}), 400
    if not password or len(password) > 128 or profanity.contains_profanity(password.lower()):
        return jsonify({"status": "Invalid or disallowed password"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO wifi_entries (name, password, downvotes, upvotes) VALUES (%s, %s, 0, 0);",
                (name, password)
            )
            conn.commit()
        return jsonify({"status": "created"}), 201
    finally:
        conn.close()

@app.route("/get-wifis", methods=["GET"])
def get_wifis():
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM wifi_entries;")
            wifis_response = cursor.fetchall()
        return jsonify(wifis_response), 200
    finally:
        conn.close()

@app.route("/downvote", methods=["POST"])
def downvote():
    wifi_id = request.args.get("id")
    if not wifi_id:
        return jsonify({"status": "invalid id"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT downvotes FROM wifi_entries WHERE id = %s;", (wifi_id,))
            wifi = cursor.fetchone()
            if not wifi:
                return jsonify({"status": "invalid id"}), 400

            if wifi["downvotes"] >= 5:
                cursor.execute("DELETE FROM wifi_entries WHERE id = %s;", (wifi_id,))
                conn.commit()
                return jsonify({"status": "wifi deleted"}), 204

            cursor.execute("UPDATE wifi_entries SET downvotes = downvotes + 1 WHERE id = %s;", (wifi_id,))
            conn.commit()
        return jsonify({"status": "updated downvotes"}), 200
    finally:
        conn.close()

@app.route("/upvote", methods=["POST"])
def upvote():
    wifi_id = request.args.get("id")
    if not wifi_id:
        return jsonify({"status": "invalid id"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT upvotes FROM wifi_entries WHERE id = %s;", (wifi_id,))
            if not cursor.fetchone():
                return jsonify({"status": "invalid id"}), 400

            cursor.execute("UPDATE wifi_entries SET upvotes = upvotes + 1 WHERE id = %s;", (wifi_id,))
            conn.commit()
        return jsonify({"status": "successfully upvoted the wifi"}), 200
    finally:
        conn.close()

@app.route("/search", methods=["GET"])
def search():
    name = request.args.get("name")
    if not name:
        return jsonify({"status": "no wifis available"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM wifi_entries WHERE name = %s;", (name,))
            wifi_response = cursor.fetchone()
        if not wifi_response:
            return jsonify({"status": "no wifis available"}), 400
        return jsonify(wifi_response), 200
    finally:
        conn.close()

@app.route("/is-in", methods=["GET"])
def is_in():
    name = request.args.get("name")
    if not name:
        return jsonify({"status": "wifi passed is invalid"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM wifi_entries WHERE name = %s;", (name,))
            returned_id = cursor.fetchone()
        if not returned_id:
            return jsonify({"status": "wifi passed is invalid"}), 400
        return jsonify({"status": "wifi passed is valid"}), 200
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)