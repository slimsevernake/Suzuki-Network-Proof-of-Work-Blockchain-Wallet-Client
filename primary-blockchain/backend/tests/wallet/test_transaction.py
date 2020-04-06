import pytest
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT

def test_transaction():
    sender_wallet = Wallet()
    recipient = "b64e8ac4"
    amount = 369
    transaction = Transaction(sender_wallet, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount

    assert "timestamp" in transaction.input
    assert transaction.input["amount"] == sender_wallet.balance
    assert transaction.input["address"] == sender_wallet.address
    assert transaction.input["public_key"] == sender_wallet.public_key

    assert Wallet.verify_signature(
        transaction.input["public_key"],
        transaction.output,
        transaction.input["signature"]
    )
   
def test_transaction_when_exceeds_balance():
    with pytest.raises(Exception, match="Input amount exceeds balance."):
        Transaction(Wallet(), "b64e8ac4", 10000)


def test_tx_update():
    sender_wallet = Wallet()
    recipient = "b64e8ac4"
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)

    next_recipient = "a13b2bf4"
    next_amount = 60

    # update Tx with new recipient
    transaction.tx_update(sender_wallet, next_recipient, next_amount)

    assert transaction.output[next_recipient] == next_amount
    assert transaction.output[sender_wallet.address] == (sender_wallet.balance - amount - next_amount)
    assert Wallet.verify_signature(
        transaction.input["public_key"],
        transaction.output,
        transaction.input["signature"]
    )

    # update Tx with existing recipient; repeat of first Tx
    transaction.tx_update(sender_wallet, recipient, amount)

    assert transaction.output[recipient] == amount * 2
    assert transaction.output[sender_wallet.address] == (sender_wallet.balance - amount * 2 - next_amount)
    assert Wallet.verify_signature(
        transaction.input["public_key"],
        transaction.output,
        transaction.input["signature"]
    )
    
def test_tx_update_when_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, "b64e8ac4", 50)

    with pytest.raises(Exception, match="Input amount exceeds balance."):
        transaction.tx_update(sender_wallet, "a13b2bf4", 10000)

def test_is_tx_valid():
    Transaction.is_tx_valid(Transaction(Wallet(), "b64e8ac4", 50))

def test_is_tx_valid_when_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, "b64e8ac4", 50)
    transaction.output[sender_wallet.address] = 9001

    with pytest.raises(Exception, match="Invalid transaction."):
       Transaction.is_tx_valid(transaction)

def test_is_tx_valid_when_invalid_sig():
    transaction = Transaction(Wallet(), "b64e8ac4", 50)
    transaction.input["signature"] = Wallet().gen_signature(transaction.output)

def test_block_reward_tx():
    wallet = Wallet()
    transaction = Transaction.generate_reward_transaction(wallet)

    assert transaction.input == MINING_REWARD_INPUT
    assert transaction.output[wallet.address] == MINING_REWARD

def test_block_reward_tx_when_valid_tx():
    reward_tx = Transaction.generate_reward_transaction(Wallet())
    Transaction.is_tx_valid(reward_tx)

def test_block_reward_tx_when_exceeds_recipients():
    reward_tx = Transaction.generate_reward_transaction(Wallet())
    reward_tx.output["second_and_invalid_recipient"] = 100

    with pytest.raises(Exception, match="Invalid block reward transaction."):
        Transaction.is_tx_valid(reward_tx)

def test_block_reward_tx_when_invalid_reward_amt():
    wallet = Wallet()
    reward_tx = Transaction.generate_reward_transaction(wallet)
    reward_tx.output[wallet.address] = 100000

    with pytest.raises(Exception, match="Invalid block reward transaction."):
        Transaction.is_tx_valid(reward_tx)
