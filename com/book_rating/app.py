from flask import Flask, jsonify, request
import mysql.connector;
import os



conn = mysql.connector.connect (
    HOST = os.environ.get("HOST"),
    USER = os.environ.get("USER"),
    DATABASE = os.environ.get("DATABASE"),
    PASSWORD = os.environ.get("PASSWORD");
)

app = Flask(__name__)
@app.route("/new-book-rate")

def new_book():
    cursor = conn.cursor()
    name = request.args.get("name")
    author = request.args.get("author")
    rating = request.args.get("rating")

    cursor.execute("SELECT * FROM book_information WHERE name = %s AND author = %s;", (name, author))
    result = cursor.fetchall()
    if not result:
        cursor.execute("UPDATE book_information SET rating = (rating + %s) / number_of_ratings WHERE name = %s AND author = %s;", (rating, name, author))
    else:
        cursor.execute("SELECT number_of_ratings FROM book_information WHERE name = %s AND author = %s;" (name, author))
        number_of_ratings = cursor.fetchall()
        number_of_ratings = number_of_ratings[0]["number_of_ratings"]
        cursor.execute("INSERT INTO book_information (name, author, number_of_ratings, rating) VALUES (%s, %s, %s, %s);" (name, author, 1))







