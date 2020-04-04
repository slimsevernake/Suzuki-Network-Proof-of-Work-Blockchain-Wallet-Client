import time
from backend.utils.generate_hash import generate_hash
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
    
    def __eq__(self, clone):
        return self.__dict__ == clone.__dict__

    def serialize_to_json(self):
        """
        Serialize a given block object into a dict comprised of its attributes.
        """
        return self.__dict__

    @staticmethod
    def mine_block(prev_block, data):
        timestamp = time.time_ns()
        prev_hash = prev_block.hash
        difficulty = Block.adjust_difficulty(prev_block, timestamp)
        nonce = 0
        hash = generate_hash(timestamp, prev_hash, data, difficulty, nonce)
        
        while (hex_to_binary(hash)[0:difficulty] != "0" * difficulty):
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(prev_block, timestamp)
            hash = generate_hash(timestamp, prev_hash, data, difficulty, nonce)
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
        if ((prev_block.difficulty -1) > 0):
            return prev_block.difficulty - 1
        return 1

    @staticmethod
    def is_block_valid(prev_block, block):
        """
        Validate each block by enforcing the following ruleset:
            - block must have proper prev_hash ref
            - block must meet proof of work requirement
            - difficulty must have adjusted by 1
            - the block has must be a valid aggregate of block fields
        """
        if (prev_block.hash != block.prev_hash):
            raise Exception("Value previous hash is invalid.")
        if (hex_to_binary(block.hash)[0:block.difficulty] != "0" * block.difficulty):
            raise Exception("Value error. A Proof of Work requirement has not been met.")
        if (abs(prev_block.difficulty - block.difficulty) > 1):
            raise Exception("Difficulty adjustment error.")

        reconstructed_hash = generate_hash(
            block.timestamp,
            block.prev_hash,
            block.data,
            block.difficulty,
            block.nonce,
        )
        if (block.hash != reconstructed_hash):
            raise Exception("Value error. A Proof of Work requirement has not been met.")

def main():
    genesis_block = Block.genesis()
    valid_block = Block.mine_block(genesis_block, 'foo')
    # block2 = Block.mine_block(block, 'bar')
    # print(block, block2)
    invalid_block = Block.mine_block(genesis_block, 'foo')
    invalid_block.prev_hash = "invalidate"
    try:
        Block.is_block_valid(genesis_block, invalid_block)
    except Exception as err:
        print(f"See err: {err}")

if __name__ == "__main__":
    main()