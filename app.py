from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

# MongoDB Atlas connection string
MONGO_URI = os.getenv('MONGODB_URI')

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select database
db = client["flask_assignment"]

# Select collection
collection = db["users"]


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Task 1: JSON API route
@app.route("/api")
def api():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "data.json")

        with open(file_path, "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# Task 2: Form submission
@app.route("/submit", methods=["POST"])
def submit():

    try:
        name = request.form.get("name")
        email = request.form.get("email")
        course = request.form.get("course")

        # Validate input
        if not name or not email or not course:
            return render_template(
                "index.html",
                error="All fields are required."
            )

        # Create document
        user_data = {
            "name": name,
            "email": email,
            "course": course
        }

        # Insert into MongoDB
        collection.insert_one(user_data)

        # Success: redirect to success page
        return redirect(url_for("success"))

    except Exception as e:

        # Error: stay on same page
        return render_template(
            "index.html",
            error=f"Error submitting data: {str(e)}"
        )


# Success page
@app.route("/success")
def success():
    return render_template("success.html")

# View data from MongoDB
@app.route("/view")
def view():
    try:
        # Fetch all documents from the collection
        data = list(collection.find({}, {"_id": 0}))  # Exclude the '_id' field

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    

if __name__ == "__main__":
    app.run(debug=True)