import pytest
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

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