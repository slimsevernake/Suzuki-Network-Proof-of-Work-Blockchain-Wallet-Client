from backend.wallet.wallet import Wallet

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
    
