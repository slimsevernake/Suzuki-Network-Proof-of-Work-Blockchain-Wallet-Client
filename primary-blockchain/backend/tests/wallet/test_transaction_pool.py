from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain

def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), "adc193bd", 1)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction

def test_purge():
    tx_pool = TransactionPool()
    tx_1 = Transaction(Wallet(), "adc193bd", 1)
    tx_2 = Transaction(Wallet(), "adc193bd", 2)
    tx_pool.set_transaction(tx_1) 
    tx_pool.set_transaction(tx_2)
    blockchain = Blockchain() 
    blockchain.add_block([
            tx_1.serialize_to_json(), 
            tx_2.serialize_to_json()])

    assert tx_1.id in tx_pool.transaction_map
    assert tx_2.id in tx_pool.transaction_map
    # purge from Pool instance any Txs written to blockchain
    tx_pool.purge(blockchain)
    assert not tx_1.id in tx_pool.transaction_map
    assert not tx_2.id in tx_pool.transaction_map