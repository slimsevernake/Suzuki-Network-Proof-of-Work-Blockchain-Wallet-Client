from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT

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

    @staticmethod
    def is_tx_chain_valid(blockchain):
        """
        Validate incoming blockchain comprised of blocks with Tx therein qua the following ruleset:
            - each Tx occurs once in the blockchain (i.e. 'double spend')
            - there is only one valid reward Tx per block 
            - transaction obj must be intrinsically valid
        """
        # Tx tracked by id, raise if duplicate
        tx_tracking_pool = set()
        # unwrap blockchain, unwrap blocks therein, deserialize ea block's Tx and parse them
        for i in range(len(blockchain)):
            block = blockchain[i]
            mining_reward_extant = False
            for serialized_tx in block.data:
                deserialized_tx = Transaction.deserialize_from_json(serialized_tx)
                # if Tx is a block reward, only validate against reward fields
                if (deserialized_tx.input == MINING_REWARD_INPUT):
                    if (mining_reward_extant):
                        raise Exception(f"""
                            There can only be one mining reward per block. 
                            Evaluation of block with hash: {block.hash} recommended.""")
                    mining_reward_extant = True
                # if Tx already exists
                if (deserialized_tx.id in tx_tracking_pool):
                    raise Exception(f"Transaction {deserialized_tx.id} is not unique; this transaction is therefore invalid.")
                # add Tx to tracking pool
                tx_tracking_pool.add(deserialized_tx.id)
                # recalc balance after every Tx to prevent input tamper
                blockchain_provenance = Blockchain()
                blockchain_provenance.chain = blockchain[0:i]
                balance_provenance = Wallet.calculate_balance(
                    blockchain_provenance,
                    deserialized_tx.input["address"]
                )

                if (balance_provenance != deserialized_tx.input["amount"]):
                    raise Exception(f"Transaction {deserialized_tx.id} contains an invalid input amount.")
                # last, run validator to check format
                Transaction.is_tx_valid(deserialized_tx)

def main(): 
    blockchain = Blockchain()
    # blockchain.add_block('one')
    # blockchain.add_block('two')

    # print(blockchain)

if __name__ == "__main__":
    main()
    