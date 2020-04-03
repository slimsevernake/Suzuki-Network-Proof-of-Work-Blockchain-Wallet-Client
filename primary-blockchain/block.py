import time
from crypto_hash import crypto_hash

class Block:
    def __init__(self, timestamp, prev_hash, hash, data):
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.hash = hash
        self.data = data

    def __repr__(self):
        return (
            "Block("
            f"timestamp: {self.timestamp}, "
            f"prev_hash: {self.prev_hash}, "
            f"hash: {self.hash}, "
            f"data: {self.data})"
        )

    @staticmethod
    def mine_block(prev_block, data):
        timestamp = time.time_ns()
        prev_hash = prev_block.hash
        hash = crypto_hash(timestamp, prev_hash, data)
        
        return Block(timestamp, prev_hash, hash, data)

    @staticmethod
    def genesis():
        return Block(1, "genesis_prev_hash", "genesis_hash",[])

def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    block2 = Block.mine_block(block, 'bar')
    print(block, block2)

if __name__ == "__main__":
    main()