import pytest
from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.blockchain.block import GENESIS_DATA

def test_blockchain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA["hash"]

def test_add_block():
    blockchain = Blockchain()
    data = "test_data"
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data

@pytest.fixture
def clone_blockchain():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block([Transaction(Wallet(), "b13b2bf4", i).serialize_to_json()])
    return blockchain

def test_is_chain_valid(clone_blockchain):
    Blockchain.is_chain_valid(clone_blockchain.chain)

def test_is_chain_valid_when_invalid_genesis(clone_blockchain):
    clone_blockchain.chain[0].hash = "invalid_hash"
    with pytest.raises(Exception, match="The genesis block must be valid."):
        Blockchain.is_chain_valid(clone_blockchain.chain)

def test_surrogate_chain(clone_blockchain):
    blockchain = Blockchain()
    blockchain.surrogate_chain(clone_blockchain.chain)

    assert blockchain.chain == clone_blockchain.chain

def test_surrogate_chain_when_insufficient_chain_len(clone_blockchain):
    blockchain = Blockchain()

    with pytest.raises(Exception, match="Chain length exception."):
        clone_blockchain.surrogate_chain(blockchain.chain) 

def test_surrogate_chain_when_invalid_chain(clone_blockchain):
    blockchain = Blockchain()
    clone_blockchain.chain[1].hash = "invalidate"

    with pytest.raises(Exception, match="Invalid chain."):
        blockchain.surrogate_chain(clone_blockchain.chain) 

def test_transaction_chain(clone_blockchain):
    Blockchain.is_tx_chain_valid(clone_blockchain.chain)

def test_transaction_chain_when_duplicate_tx(clone_blockchain):
    tx_instance = Transaction(Wallet(), "b13b2bf4", 1).serialize_to_json()
    clone_blockchain.add_block([tx_instance, tx_instance])

    with pytest.raises(Exception, match="is not unique;"):
        Blockchain.is_tx_chain_valid(clone_blockchain.chain)

def test_transaction_chain_when_duplicate_rewards(clone_blockchain):
    reward_1 = Transaction.generate_reward_transaction(Wallet()).serialize_to_json()
    reward_2 = Transaction.generate_reward_transaction(Wallet()).serialize_to_json()
    clone_blockchain.add_block([reward_1, reward_2])

    with pytest.raises(Exception, match="There can only be one mining reward per block."):
        Blockchain.is_tx_chain_valid(clone_blockchain.chain)

def test_transaction_chain_when_tx_malformatted(clone_blockchain):
    malformed_tx_instance = Transaction(Wallet(), "b13b2bf4", 1)
    # sign with different wallet
    malformed_tx_instance.input["signature"] = Wallet().gen_signature(malformed_tx_instance.output)
    clone_blockchain.add_block([malformed_tx_instance.serialize_to_json()])

    with pytest.raises(Exception):
        Blockchain.is_tx_chain_valid(clone_blockchain.chain)

def test_transaction_chain_when_invalid_balance_provenance(clone_blockchain):
    wallet = Wallet()
    malformed_tx_instance = Transaction(Wallet(), "b13b2bf4", 1)
    malformed_tx_instance.output[wallet.address] = 9000
    malformed_tx_instance.input["amount"] = 9001
    malformed_tx_instance.input["signature"] = wallet.gen_signature(malformed_tx_instance.output)

    clone_blockchain.add_block(malformed_tx_instance.serialize_to_json())

    with pytest.raises(Exception, match="contains an invalid input amount"):
        Blockchain.is_tx_chain_valid(clone_blockchain.chain)

