"""
Deliberately INSECURE sample for Week 2 scanning practice.
Do NOT copy these patterns into real code. Find them with SAST + secret scanning.
"""
import ipaddress
import os
import sqlite3
import subprocess

from argon2 import PasswordHasher
from flask import Flask, request

app = Flask(__name__)

AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
PASSWORD_HASHER = PasswordHasher()

@app.route("/user")
def user():
    name = request.args.get("name", "")
    with sqlite3.connect("app.db") as con:
        rows = con.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()
    return str(rows)

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return "invalid IP address", 400
    return subprocess.check_output(["ping", "-c", "1", host], text=True)

def store_password(pw):
    return PASSWORD_HASHER.hash(pw)

if __name__ == "__main__":
    app.run(debug=False)
