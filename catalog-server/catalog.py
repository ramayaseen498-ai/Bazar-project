from flask import Flask, jsonify, request
import csv
import os

app = Flask(__name__)

CATALOG_FILE = 'catalog.csv'

#  READ CSV
def read_books():
    books = []
    with open(CATALOG_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append({
                'id': int(row['id']),
                'title': row['title'],
                'topic': row['topic'],
                'price': float(row['price']),
                'quantity': int(row['quantity'])
            })
    return books

# WRITE CSV
def write_books(books):
    with open(CATALOG_FILE, 'w', newline='') as f:
        fieldnames = ['id', 'title', 'topic', 'price', 'quantity']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

# search by topic
@app.route('/search/<topic>', methods=['GET'])
def search(topic):
    books = read_books()
    result = [{'id': b['id'], 'title': b['title']} 
              for b in books if b['topic'] == topic]
    return jsonify(result)

# info by id
@app.route('/info/<int:item_id>', methods=['GET'])
def info(item_id):
    books = read_books()
    for b in books:
        if b['id'] == item_id:
            return jsonify({
                'title': b['title'],
                'price': b['price'],
                'quantity': b['quantity']
            })
    return jsonify({'error': 'Book not found'}), 404

# update quantity or price
@app.route('/update/<int:item_id>', methods=['PUT'])
def update(item_id):
    books = read_books()
    data = request.json
    for b in books:
        if b['id'] == item_id:
            if 'quantity' in data:
                b['quantity'] += data['quantity']
            if 'price' in data:
                b['price'] = data['price']
            write_books(books)
            return jsonify({'message': 'Updated successfully'})
    return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)