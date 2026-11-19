from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import secrets
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


def hash_auth_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def get_bearer_token():
    authorization = request.headers.get("Authorization", "")

    if not authorization.startswith("Bearer "):
        return None

    token = authorization[7:].strip()
    return token or None


def get_authenticated_user():
    token = get_bearer_token()

    if not token:
        return None

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT users.id, users.username, users.is_admin
                FROM auth_tokens
                JOIN users ON users.id = auth_tokens.user_id
                WHERE auth_tokens.token_hash = %s
                  AND auth_tokens.expires_at > UTC_TIMESTAMP();
                """,
                (hash_auth_token(token),)
            )
            return cursor.fetchone()
    finally:
        conn.close()


# Create required tables and safely add columns to existing installations.
init_conn = get_db()
try:
    with init_conn.cursor() as setup_cursor:
        setup_cursor.execute("""
        CREATE TABLE IF NOT EXISTS wifi_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            password VARCHAR(255),
            downvotes INT NOT NULL DEFAULT 0,
            upvotes INT NOT NULL DEFAULT 0,
            submitted_by_user_id INT NULL,
            approved TINYINT(1) NOT NULL DEFAULT 0
        );
        """)

        setup_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(32) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            is_admin TINYINT(1) NOT NULL DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)

        setup_cursor.execute("""
        CREATE TABLE IF NOT EXISTS wifi_downvotes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            wifi_id INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY one_downvote_per_user (user_id, wifi_id)
        );
        """)

        setup_cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_tokens (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            token_hash CHAR(64) NOT NULL UNIQUE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL
        );
        """)

        # Existing entries stay public after upgrading. New entries are inserted
        # with approved=0 explicitly in /new-entry.
        setup_cursor.execute(
            "SHOW COLUMNS FROM wifi_entries LIKE 'submitted_by_user_id';"
        )
        if not setup_cursor.fetchone():
            setup_cursor.execute(
                "ALTER TABLE wifi_entries "
                "ADD COLUMN submitted_by_user_id INT NULL;"
            )

        setup_cursor.execute("SHOW COLUMNS FROM wifi_entries LIKE 'approved';")
        if not setup_cursor.fetchone():
            setup_cursor.execute(
                "ALTER TABLE wifi_entries "
                "ADD COLUMN approved TINYINT(1) NOT NULL DEFAULT 1;"
            )

        setup_cursor.execute("SHOW COLUMNS FROM users LIKE 'is_admin';")
        if not setup_cursor.fetchone():
            setup_cursor.execute(
                "ALTER TABLE users "
                "ADD COLUMN is_admin TINYINT(1) NOT NULL DEFAULT 0;"
            )

        init_conn.commit()
finally:
    init_conn.close()


app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "https://opensignal-wifi.vercel.app"
            ]
        }
    },
    supports_credentials=True
)

profanity.load_censor_words()

BLOCKED_TERMS = {
    "goon", "gooning", "skibidi", "gyatt", "rizz",
    "diddy", "spam", "stupid", "idiot", "dumb", "goona"
}


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


def require_admin():
    user = get_authenticated_user()
    if not user:
        return None, (jsonify({"status": "not logged in"}), 401)
    if not user.get("is_admin"):
        return None, (jsonify({"status": "admin access required"}), 403)
    return user, None


@app.route("/signup", methods=["POST"])
def signup():
    username = (request.args.get("username") or "").strip()
    password = request.args.get("password") or ""

    if not re.fullmatch(r"[A-Za-z0-9_]{3,32}", username):
        return jsonify({
            "status": "Username must be 3–32 letters, numbers, or underscores"
        }), 400

    if len(password) < 8 or len(password) > 128:
        return jsonify({"status": "Password must be 8–128 characters"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s);",
                (
                    username,
                    generate_password_hash(password, method="pbkdf2:sha256")
                )
            )
            conn.commit()

        return jsonify({"status": "account created"}), 201
    except pymysql.err.IntegrityError:
        return jsonify({"status": "username already exists"}), 409
    finally:
        conn.close()


@app.route("/login", methods=["POST"])
def login():
    username = (request.args.get("username") or "").strip()
    password = request.args.get("password") or ""

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, password_hash FROM users WHERE username = %s;",
                (username,)
            )
            user = cursor.fetchone()

        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({"status": "invalid username or password"}), 401

        token = secrets.token_urlsafe(32)

        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM auth_tokens WHERE expires_at <= UTC_TIMESTAMP();"
            )
            cursor.execute(
                """
                INSERT INTO auth_tokens (user_id, token_hash, expires_at)
                VALUES (%s, %s, DATE_ADD(UTC_TIMESTAMP(), INTERVAL 30 DAY));
                """,
                (user["id"], hash_auth_token(token))
            )
            conn.commit()

        return jsonify({
            "status": "logged in",
            "token": token,
            "user": {
                "id": user["id"],
                "username": user["username"]
            }
        }), 200
    finally:
        conn.close()


@app.route("/logout", methods=["POST"])
def logout():
    token = get_bearer_token()

    if not token:
        return jsonify({"status": "logged out"}), 200

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM auth_tokens WHERE token_hash = %s;",
                (hash_auth_token(token),)
            )
            conn.commit()
        return jsonify({"status": "logged out"}), 200
    finally:
        conn.close()


@app.route("/me", methods=["GET"])
def me():
    user = get_authenticated_user()

    if not user:
        return jsonify({"status": "not logged in"}), 401

    return jsonify({"user": user}), 200


@app.route("/new-entry", methods=["POST"])
def new_wifi_entry():
    user = get_authenticated_user()
    if not user:
        return jsonify({"status": "log in before adding a network"}), 401

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
                """
                INSERT INTO wifi_entries
                    (name, password, downvotes, upvotes, submitted_by_user_id, approved)
                VALUES (%s, %s, 0, 0, %s, 0);
                """,
                (name, password, user["id"])
            )
            conn.commit()

        return jsonify({"status": "submitted for approval"}), 201
    finally:
        conn.close()


@app.route("/get-wifis", methods=["GET"])
def get_wifis():
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT wifi_entries.*,
                       users.username AS submitted_by
                FROM wifi_entries
                LEFT JOIN users ON users.id = wifi_entries.submitted_by_user_id
                WHERE wifi_entries.approved = 1;
                """
            )
            wifis_response = cursor.fetchall()

        return jsonify(wifis_response), 200
    finally:
        conn.close()


@app.route("/pending-wifis", methods=["GET"])
def pending_wifis():
    user, error = require_admin()
    if error:
        return error

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT wifi_entries.*,
                       users.username AS submitted_by
                FROM wifi_entries
                LEFT JOIN users ON users.id = wifi_entries.submitted_by_user_id
                WHERE wifi_entries.approved = 0
                ORDER BY wifi_entries.id DESC;
                """
            )
            rows = cursor.fetchall()

        return jsonify(rows), 200
    finally:
        conn.close()


@app.route("/approve-entry", methods=["POST"])
def approve_entry():
    user, error = require_admin()
    if error:
        return error

    entry_id = request.args.get("id", type=int)
    if not entry_id:
        return jsonify({"status": "invalid id"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE wifi_entries SET approved = 1 WHERE id = %s AND approved = 0;",
                (entry_id,)
            )
            if cursor.rowcount == 0:
                conn.rollback()
                return jsonify({"status": "pending entry not found"}), 404
            conn.commit()

        return jsonify({"status": "entry approved"}), 200
    finally:
        conn.close()


@app.route("/reject-entry", methods=["POST"])
def reject_entry():
    user, error = require_admin()
    if error:
        return error

    entry_id = request.args.get("id", type=int)
    if not entry_id:
        return jsonify({"status": "invalid id"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM wifi_entries WHERE id = %s AND approved = 0;",
                (entry_id,)
            )
            if cursor.rowcount == 0:
                conn.rollback()
                return jsonify({"status": "pending entry not found"}), 404
            conn.commit()

        return jsonify({"status": "entry rejected"}), 200
    finally:
        conn.close()


@app.route("/downvote", methods=["POST"])
def downvote():
    user = get_authenticated_user()
    wifi_id = request.args.get("id", type=int)

    if not user:
        return jsonify({"status": "log in before reporting a network"}), 401

    if not wifi_id:
        return jsonify({"status": "invalid id"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, downvotes FROM wifi_entries WHERE id = %s AND approved = 1 FOR UPDATE;",
                (wifi_id,)
            )
            wifi = cursor.fetchone()

            if not wifi:
                conn.rollback()
                return jsonify({"status": "invalid id"}), 400

            try:
                cursor.execute(
                    """
                    INSERT INTO wifi_downvotes (user_id, wifi_id)
                    VALUES (%s, %s);
                    """,
                    (user["id"], wifi_id)
                )
            except pymysql.err.IntegrityError:
                conn.rollback()
                return jsonify({
                    "status": "you have already reported this network"
                }), 409

            if wifi["downvotes"] + 1 >= 5:
                cursor.execute(
                    "DELETE FROM wifi_downvotes WHERE wifi_id = %s;",
                    (wifi_id,)
                )
                cursor.execute(
                    "DELETE FROM wifi_entries WHERE id = %s;",
                    (wifi_id,)
                )
                conn.commit()
                return "", 204

            cursor.execute(
                """
                UPDATE wifi_entries
                SET downvotes = downvotes + 1
                WHERE id = %s AND approved = 1;
                """,
                (wifi_id,)
            )
            conn.commit()

        return jsonify({"status": "updated downvotes"}), 200
    finally:
        conn.close()


@app.route("/upvote", methods=["POST"])
def upvote():
    wifi_id = request.args.get("id", type=int)

    if not wifi_id:
        return jsonify({"status": "invalid id"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT upvotes FROM wifi_entries WHERE id = %s AND approved = 1;",
                (wifi_id,)
            )

            if not cursor.fetchone():
                return jsonify({"status": "invalid id"}), 400

            cursor.execute(
                """
                UPDATE wifi_entries
                SET upvotes = upvotes + 1
                WHERE id = %s AND approved = 1;
                """,
                (wifi_id,)
            )
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
            cursor.execute(
                "SELECT * FROM wifi_entries WHERE name = %s AND approved = 1;",
                (name,)
            )
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
            cursor.execute(
                "SELECT id FROM wifi_entries WHERE name = %s AND approved = 1;",
                (name,)
            )
            returned_id = cursor.fetchone()

        if not returned_id:
            return jsonify({"status": "wifi passed is invalid"}), 400

        return jsonify({"status": "wifi passed is valid"}), 200
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
