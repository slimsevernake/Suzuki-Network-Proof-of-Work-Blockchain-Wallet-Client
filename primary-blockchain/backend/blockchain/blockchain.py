from backend.blockchain.block import Block

class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        prev_block = self.chain[-1]
        self.chain.append(Block.mine_block(prev_block, data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'
    
    def surrogate_chain(self, incoming_chain):
        """
        Surrogate local instance chain with that of incoming/proposal instance, contingent on the following ruleset:
            - Len of incoming chain instance must exceed that of local instance;
            - Incoming chain is formatted such that it is valid
        """
        if (len(incoming_chain) <= len(self.chain)):
            raise Exception("Chain length exception. Surrogation requirements have not been met.")
        try:
            Blockchain.is_chain_valid(incoming_chain)
        except Exception as err:
             raise Exception(f"Invalid chain. Surrogation requirements have not been met. See err: {err}")
        
        self.chain = incoming_chain

    def serialize_to_json(self):
        """
        Serialize a given blockchain instance into an enum of blocks.
        """ 
        
        return list(map(lambda block: block.serialize_to_json(), self.chain))
    
    @staticmethod
    def deserialize_from_json(serialized_blockchain_obj):
        """
        De-serialize a given list of serialized blocks into a Blockchain instance.
        """
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda serialized_block_obj: Block.deserialize_from_json(serialized_block_obj), serialized_blockchain_obj)
        )
        return blockchain

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
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)

if __name__ == "__main__":
    main()
    