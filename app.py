from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["flask_mongodb_db"]
collection = db["submissions"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            raise ValueError("All fields are required.")

        document = {
            "name": name,
            "email": email,
            "message": message
        }

        collection.insert_one(document)

        return redirect(url_for("success"))

    except Exception as error:
        return render_template(
            "index.html",
            error=str(error),
            name=request.form.get("name", ""),
            email=request.form.get("email", ""),
            message=request.form.get("message", "")
        )


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)