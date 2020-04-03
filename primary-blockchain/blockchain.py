from block import Block

class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        prev_block = self.chain[-1]
        self.chain.append(Block.mine_block(prev_block, data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

def main():
    blockchain = Blockchain()
    for n in range(10):
         blockchain.add_block(n)

    print(blockchain)

if __name__ == "__main__":
    main()
    