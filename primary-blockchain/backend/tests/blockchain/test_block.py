from backend.blockchain.block import Block, GENESIS_DATA

def test_mine_block():
   prev_block = Block.genesis()
   data = "test"
   block = Block.mine_block(prev_block, data)

   assert isinstance(block, Block)
   assert block.data == data
   assert block.prev_hash == prev_block.hash
   assert block.hash[0:block.difficulty] == "0" * block.difficulty

def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value

