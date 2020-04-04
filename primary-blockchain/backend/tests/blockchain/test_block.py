import time
import pytest
from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.utils.hex_to_binary import hex_to_binary

def test_mine_block():
   prev_block = Block.genesis()
   data = "test"
   block = Block.mine_block(prev_block, data)

   assert isinstance(block, Block)
   assert block.data == data
   assert block.prev_hash == prev_block.hash
   assert hex_to_binary(block.hash)[0:block.difficulty] == "0" * block.difficulty

def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value

def test_quickly_mined_block():
    prev_block = Block.mine_block(Block.genesis(), "foo")
    mined_block = Block.mine_block(prev_block, "bar")

    assert mined_block.difficulty == prev_block.difficulty + 1

def test_slowly_mined_block():
    prev_block = Block.mine_block(Block.genesis(), "foo")
    # force mining rate
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(prev_block, "bar")
    assert mined_block.difficulty == prev_block.difficulty - 1

def test_mined_block_difficulty_static():
    prev_block = Block(
        time.time_ns(),
        "test_prev_hash",
        "test_hash",
        "test_data",
        1,
        0
    )
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(prev_block, "bar")
    assert mined_block.difficulty == 1

@pytest.fixture
def prev_block():
    return Block.genesis()

@pytest.fixture
def block(prev_block):
    return Block.mine_block(prev_block, "test_data")

def test_is_block_valid(prev_block, block):
    Block.is_block_valid(prev_block, block)

def test_is_block_valid_with_invalid_prev_hash(prev_block, block):
    block.prev_hash = "invalidate"

    with pytest.raises(Exception, match="Value previous hash is invalid."):
        Block.is_block_valid(prev_block, block)

def test_is_block_valid_with_invalid_proof_of_work(prev_block, block):
    block.hash = "fff" 

    with pytest.raises(Exception, match="Value error. A Proof of Work requirement has not been met."):
        Block.is_block_valid(prev_block, block)

def test_is_block_valid_with_maladjusted_difficulty(prev_block, block):
    adjusted_difficulty = 10
    block.difficulty = adjusted_difficulty
    block.hash = f"{'0' * adjusted_difficulty}abc123"

    with pytest.raises(Exception, match="Difficulty adjustment error."):
        Block.is_block_valid(prev_block, block)

def test_is_block_valid_with_invalid_hash(prev_block, block):
    block.hash = "000000000000000abc123"

    with pytest.raises(Exception, match="Value error. A Proof of Work requirement has not been met."):
        Block.is_block_valid(prev_block, block)