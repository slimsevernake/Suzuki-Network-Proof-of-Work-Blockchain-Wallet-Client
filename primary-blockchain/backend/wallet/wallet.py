import uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from backend.config import INITIAL_BALANCE


class Wallet:
    """
    A wallet, or balance aggregation object for miners/node operators.
        - Maintains local record of its owner's balance
        - Enables owner to authorize transactions on the network.
    """
    def __init__(self):
        self.address = str(uuid.uuid4())[0:8] # 8 digit still affords 3T possible addresses
        self.balance = INITIAL_BALANCE
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(), # Koblitz I: prime-generated curve represented in 256 binary bits
            default_backend()) 
        self.public_key = self.private_key.public_key() # extrapolate pubkey

def main():
    wallet = Wallet()
    print(f"Wallet: {wallet.__dict__}")

if __name__ == "__main__":
    main()