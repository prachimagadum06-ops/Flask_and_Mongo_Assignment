from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable is not set")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")
    print("MongoDB Atlas connection successful.")

    db = client["flask_mongodb_db"]
    collection = db["submissions"]

except Exception as error:
    print("MongoDB Atlas connection failed:", error)
    raise


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except FileNotFoundError:
        return jsonify({
            "error": "data.json file not found"
        }), 404

    except json.JSONDecodeError:
        return jsonify({
            "error": "Invalid JSON format in data.json"
        }), 500

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        errors = []

        if not name:
            errors.append("Name is required.")
        elif len(name) < 2:
            errors.append("Name must contain at least 2 characters.")
        elif len(name) > 50:
            errors.append("Name must not exceed 50 characters.")

        if not email:
            errors.append("Email is required.")
        elif "@" not in email or "." not in email.split("@")[-1]:
            errors.append("Please enter a valid email address.")

        if not message:
            errors.append("Message is required.")
        elif len(message) < 5:
            errors.append("Message must contain at least 5 characters.")
        elif len(message) > 500:
            errors.append("Message must not exceed 500 characters.")

        if errors:
            return render_template(
                "index.html",
                errors=errors,
                name=name,
                email=email,
                message=message
            ), 400

        document = {
            "name": name,
            "email": email,
            "message": message
        }

        collection.insert_one(document)

        return redirect(url_for("success"))

    except Exception as error:
        print("Form submission error:", error)

        return render_template(
            "index.html",
            error="An unexpected error occurred. Please try again.",
            name=request.form.get("name", ""),
            email=request.form.get("email", ""),
            message=request.form.get("message", "")
        ), 500


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)