import os
import random
import requests
from flask import Flask, jsonify, request
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet()
pubsub = PubSub(blockchain)

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

    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    
    return jsonify(block.serialize_to_json())

@app.route("/wallet/transact", methods=["POST"])
def wallet_transaction_route():
    tx_data = request.get_json()
    transaction = Transaction(
        wallet,
        tx_data["recipient"],
        tx_data["amount"]
    )
    return jsonify(transaction.serialize_to_json())

ROOT_PORT = 5000
PORT = ROOT_PORT

# peer instance, supports up to 1,000 peers
if os.environ.get("PEER") == "True":
    PORT = random.randint(5001, 6000)

    # fetch blockchain instance
    res = requests.get(f"http://localhost:{ROOT_PORT}/blockchain")
    res_blockchain = Blockchain.deserialize_from_json(res.json())
    try:
        blockchain.surrogate_chain(res_blockchain)
        print("\n -- Successfully synchronized local blockchain instance.")
    except Exception as err:
        print(f"\n -- Error synchronizing local blockchain instance. See: {err}")

app.run(port=PORT)