from flask import Flask, jsonify, request
import mysql.connector;


conn = mysql.connector.connect (
    
)

app = Flask(__name__)
@app.route("/new-book")

def new_book():
    request.args.get("name")
    request.args.get("author")
    request.args.get("rating")


