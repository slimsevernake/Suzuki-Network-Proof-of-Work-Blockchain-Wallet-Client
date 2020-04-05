from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

for i in range(10):
    blockchain.add_block(i)

@app.route("/")
def default_route():
    return "Welcome"

@app.route("/blockchain")
def blockchain_route():
    return jsonify(blockchain.serialize_to_json())

@app.route("/blockchain/mine")
def mine_block_route():
    transaction_data = "tx_data"
    blockchain.add_block(transaction_data)
    return jsonify(blockchain.chain[-1].serialize_to_json())

app.run()