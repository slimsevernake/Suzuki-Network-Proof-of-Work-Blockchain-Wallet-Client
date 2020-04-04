import time
from backend.utils.crypto_hash import crypto_hash
from backend.utils.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
    "timestamp": 1,
    "prev_hash": "genesis_prev_hash",
    "hash": "genesis_hash",
    "data": [],
    "difficulty": 3,
    "nonce": "genesis_nonce"
}

class Block:
    def __init__(self, timestamp, prev_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            "Block("
            f"timestamp: {self.timestamp}, "
            f"prev_hash: {self.prev_hash}, "
            f"hash: {self.hash}, "
            f"data: {self.data}), "
            f"difficulty: {self.difficulty}), "
            f"nonce: {self.nonce})"
        )

    @staticmethod
    def mine_block(prev_block, data):
        timestamp = time.time_ns()
        prev_hash = prev_block.hash
        difficulty = Block.adjust_difficulty(prev_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, prev_hash, data, difficulty, nonce)
        
        while (hex_to_binary(hash)[0:difficulty] != "0" * difficulty):
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(prev_block, timestamp)
            hash = crypto_hash(timestamp, prev_hash, data, difficulty, nonce)
        return Block(timestamp, prev_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty(prev_block, current_block_timestamp):
        """
        Calculate adjusted difficulty contingent on global var MINE_RATE,
        such that the difficulty is incremented/decremented to produce
        a block-mining throughput of 1 block/ 4 seconds
        """
        if ((current_block_timestamp - prev_block.timestamp) < MINE_RATE):
            return prev_block.difficulty + 1
        # prevent difficulty from dropping below 0
        if (prev_block.difficulty -1) > 0:
            return prev_block.difficulty - 1
        return 1

def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    block2 = Block.mine_block(block, 'bar')
    print(block, block2)

if __name__ == "__main__":
    main()