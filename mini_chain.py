def lightning_hash(data):
    return data + "*"



class Block:
  def __init__(self, data, hash, last_hash):
    self.data = data
    self.hash = hash
    self.last_hash = last_hash 


foo_block = Block('foodata','foohash','lastfoohash')

print(foo_block.data)
print(foo_block.hash)
print(foo_block.last_hash)