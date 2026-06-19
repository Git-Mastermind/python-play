from flask import Flask, jsonify, request
import mysql.connector

digital_nomad_db = mysql.connector.connect()