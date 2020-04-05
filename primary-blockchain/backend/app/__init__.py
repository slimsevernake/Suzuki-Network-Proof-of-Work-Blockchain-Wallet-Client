import os
import random
from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub()

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

PORT = 5000

# peer instance, supports up to 1,000 peers
if os.environ.get("PEER") == "True":
    PORT = random.randint(5001, 6000)
    
app.run(port=PORT)