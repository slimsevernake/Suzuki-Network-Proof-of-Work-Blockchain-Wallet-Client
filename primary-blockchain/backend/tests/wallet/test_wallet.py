from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.blockchain.blockchain import Blockchain
from backend.config import INITIAL_BALANCE

def test_verify_signature_with_valid_signature():
    data = { "foo" : "bar" }
    wallet = Wallet()
    sig = wallet.gen_signature(data)

    assert Wallet.verify_signature(wallet.public_key, data, sig)

def test_verify_signature_with_invalid_signature():
    data = { "foo" : "bar" }
    wallet = Wallet()
    sig = wallet.gen_signature(data)

    assert not Wallet.verify_signature(Wallet().public_key, data, sig)
    
def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    # NEW: new Wallet() `wallet` should have initial balance
    assert Wallet.calculate_balance(blockchain, wallet.address) == INITIAL_BALANCE
    
    sent_amt = 50
    outgoing_transaction = Transaction(wallet, "a13b2bf4", sent_amt) # send to `wallet` from "a13b2bf4"
    blockchain.add_block([outgoing_transaction.serialize_to_json()])
    # SEND: `wallet` should have initial balance sans amt 
    assert Wallet.calculate_balance(blockchain, wallet.address) == INITIAL_BALANCE - sent_amt

    received_amt_1 = 25
    incoming_transaction_1 = Transaction(Wallet(), wallet.address, received_amt_1) # receive by `wallet` from new Wallet()
    received_amt_2 = 77
    incoming_transaction_2 = Transaction(Wallet(), wallet.address, received_amt_2)
    blockchain.add_block(
        [incoming_transaction_1.serialize_to_json(), 
        incoming_transaction_2.serialize_to_json()]
    )
    # RECEIVE: `wallet` should have initial balance plus incoming amt(s) 
    assert Wallet.calculate_balance(blockchain, wallet.address) == INITIAL_BALANCE - sent_amt + received_amt_1 + received_amt_2