import os
import random
import requests
from backend.config import FRONTEND_ADDRESS
from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

app = Flask(__name__)
CORS(app, resources={ r"/*": { "origins": f"{FRONTEND_ADDRESS}"} })  # add CORS Policy for all endpoints
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)

@app.route("/")
def default_route():
    return "Welcome"

@app.route("/blockchain")
def blockchain_route():
    return jsonify(blockchain.serialize_to_json())

@app.route("/blockchain/range")
def paginate_blockchain_route():
    # http://localhost:5000/blockchain/range?start={start}&end={end}
    start = int(request.args.get("start"))
    end = int(request.args.get("end"))
    # return reversed list to display most recent first
    return jsonify(blockchain.serialize_to_json()[::-1][start:end]) 

# fetch len of blockchain to determine pagination num
@app.route("/blockchain/length")
def len_blockchain_route():
    return jsonify(len(blockchain.chain))

@app.route("/blockchain/mine")
def mine_block_route():
    """
    Mine blocks on the shared chain. If given wallet is first to validate a given block, 
    `prospective_mining_reward` will be allocated into given wallet UTXO. Else, the reward 
    transaction will be void.
    """
    # serialize all Tx 
    tx_data = transaction_pool.serialize_to_json()
    # generate, serialize mining reward transaction obj
    prospective_mining_reward = Transaction.generate_reward_transaction(wallet).serialize_to_json()
    # append reward Tx and submit
    tx_data.append(prospective_mining_reward)
    blockchain.add_block(tx_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.purge(blockchain)
    
    return jsonify(block.serialize_to_json())

# @app.route("/wallet")
# def wallet_route():
#     return wallet.balance

@app.route("/wallet/transact", methods=["POST"])
def wallet_transaction_route():
    tx_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)
    
    if transaction:
        transaction.tx_update(
        wallet,
        tx_data["recipient"],
        tx_data["amount"]
    )
    else:
        transaction = Transaction(
            wallet,
            tx_data["recipient"],
            tx_data["amount"]
        )
    
    pubsub.broadcast_transaction(transaction)

    return jsonify(transaction.serialize_to_json())

@app.route("/wallet/info")
def wallet_info_route():
    return jsonify({"Address" : wallet.address, "Balance" : wallet.balance})

@app.route("/known-addresses")
def known_addresses_route():
    known_addresses = set()
    for block in blockchain.chain:
        for tx in block.data:
            known_addresses.update(tx["output"].keys())

    return jsonify(list(known_addresses))


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

# seeded test instance - creates 10 blocks w/2 Tx ea
if os.environ.get("SEED") == "True":
    for i in range(10):
        blockchain.add_block([
            Transaction(Wallet(),Wallet().address, random.randint(2, 50)).serialize_to_json(),
            Transaction(Wallet(),Wallet().address, random.randint(2, 50)).serialize_to_json()
        ])

app.run(port=PORT)