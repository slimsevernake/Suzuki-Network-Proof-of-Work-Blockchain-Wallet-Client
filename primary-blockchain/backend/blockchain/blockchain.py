from backend.blockchain.block import Block

class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        prev_block = self.chain[-1]
        self.chain.append(Block.mine_block(prev_block, data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'
    
    @staticmethod
    def is_chain_valid(blockchain):
        """
        Validate incoming blockchain qua the following ruleset:
            - the blockchain must begin with a valid genesis block
            - blocks must be formatted properly
        """
        if (blockchain[0] != Block.genesis()):
            raise Exception("The genesis block must be valid.")

        for i in range(1,len(blockchain)):
            block = blockchain[i]
            prev_block = blockchain[i -1]
            Block.is_block_valid(prev_block, block)

def main(): 
    blockchain = Blockchain()
    for n in range(10):
         blockchain.add_block(n)

    print(blockchain)

if __name__ == "__main__":
    main()
    