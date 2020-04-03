import time
from backend.utils.crypto_hash import crypto_hash

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
        difficulty = prev_block.difficulty
        nonce = 0
        hash = crypto_hash(timestamp, prev_hash, data, difficulty, nonce)
        
        while hash[0:difficulty] != "0" * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            hash = crypto_hash(timestamp, prev_hash, data, difficulty, nonce)
        return Block(timestamp, prev_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        return Block(**GENESIS_DATA)

def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    block2 = Block.mine_block(block, 'bar')
    print(block, block2)

if __name__ == "__main__":
    main()