import pytest
from backend.blockchain.blockchain import Blockchain
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
        blockchain.add_block(i)
    return blockchain

def test_is_chain_valid(clone_blockchain):
    Blockchain.is_chain_valid(clone_blockchain.chain)

def test_is_chain_valid_with_invalid_genesis(clone_blockchain):
    clone_blockchain.chain[0].hash = "invalid_hash"
    with pytest.raises(Exception, match="The genesis block must be valid."):
        Blockchain.is_chain_valid(clone_blockchain.chain)
