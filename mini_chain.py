def lightning_hash(data):
    return data + "*"

class Block:
  def __init__(self, data, hash, prev_hash):
    self.data = data
    self.hash = hash
    self.prev_hash = prev_hash

class Blockchain:
    def __init__(self):
        self.chain = []
        genesis = Block('gen_data', 'gen_hash', 'gen_prev_hash')
        
        self.chain = [genesis]

    def add_block(self, data):
        prev_hash = self.chain[-1].hash
        hash = lightning_hash(data + prev_hash)
        block = Block(data, hash, prev_hash)

        self.chain.append(block)

foo_blockchain = Blockchain()
foo_blockchain.add_block('one')
foo_blockchain.add_block('two')
foo_blockchain.add_block('three')
foo_blockchain.add_block('four')
foo_blockchain.add_block('five')
foo_blockchain.add_block('six')

for block in foo_blockchain.chain:
    print(block.__dict__)
