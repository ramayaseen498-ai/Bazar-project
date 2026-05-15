from flask import Flask, jsonify   
import csv                          
import os                           
import threading                   
import requests                     

app = Flask(__name__)               

CATALOG_URL = os.environ.get("CATALOG_URL", "http://localhost:5001")
ORDERS_FILE = "orders.csv"       
lock = threading.Lock()        


def get_next_order_id():
    with open(ORDERS_FILE, newline="") as f:
        rows = list(csv.reader(f))
        return len(rows)


def log_order(order_id, item_id, title):
    with open(ORDERS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([order_id, item_id, title])


@app.route("/purchase/<int:item_id>", methods=["POST"])
def purchase(item_id):
    with lock: 
        try:
            resp = requests.get(f"{CATALOG_URL}/info/{item_id}")
        except requests.exceptions.ConnectionError:
            return jsonify({"error": "Catalog server unreachable"}), 503

        if resp.status_code == 404:
            return jsonify({"error": "Item not found"}), 404

        book = resp.json() 

        if book["quantity"] <= 0:
            return jsonify({"error": f"'{book['title']}' is out of stock"}), 409

        requests.put(
            f"{CATALOG_URL}/update/{item_id}",
            json={"quantity": -1}   
        )

        order_id = get_next_order_id()
        log_order(order_id, item_id, book["title"])

        print(f"bought book {book['title']}")  
        return jsonify({
            "message": f"bought book {book['title']}",
            "order_id": order_id
        }), 200       


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)