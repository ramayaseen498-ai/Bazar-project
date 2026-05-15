from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

CATALOG_URL = os.environ.get("CATALOG_URL", "http://localhost:5001")
ORDER_URL   = os.environ.get("ORDER_URL",   "http://localhost:5002")


@app.route("/search/<topic>", methods=["GET"])
def search(topic):
    resp = requests.get(f"{CATALOG_URL}/search/{topic}")
    return jsonify(resp.json()), resp.status_code


@app.route("/info/<int:item_id>", methods=["GET"])
def info(item_id):
    resp = requests.get(f"{CATALOG_URL}/info/{item_id}")
    return jsonify(resp.json()), resp.status_code


@app.route("/purchase/<int:item_id>", methods=["POST"])
def purchase(item_id):
    resp = requests.post(f"{ORDER_URL}/purchase/{item_id}")
    return jsonify(resp.json()), resp.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)