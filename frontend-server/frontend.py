from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

# Service URLs
CATALOG_URL = os.environ.get("CATALOG_URL", "http://catalog:5001")
ORDER_URL = os.environ.get("ORDER_URL", "http://order:5002")


# Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Frontend Service is Running"
    })


# Search Route
@app.route("/search/<topic>", methods=["GET"])
def search(topic):
    response = requests.get(f"{CATALOG_URL}/search/{topic}")
    return jsonify(response.json()), response.status_code


# Item Information Route
@app.route("/info/<int:item_id>", methods=["GET"])
def info(item_id):
    response = requests.get(f"{CATALOG_URL}/info/{item_id}")
    return jsonify(response.json()), response.status_code


# Purchase Route
@app.route("/purchase/<int:item_id>", methods=["POST"])
def purchase(item_id):
    response = requests.post(f"{ORDER_URL}/purchase/{item_id}")
    return jsonify(response.json()), response.status_code


# Run Application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)