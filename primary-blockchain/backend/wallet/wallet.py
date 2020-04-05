import uuid
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
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

    def gen_signature(self, data):
        """
        Utilizes the local private key to generate a signature for a given input obj,`data`.
        Returns as signature obj.
        """
        return self.private_key.sign(
            json.dumps(data).encode("utf-8"),
            ec.ECDSA(hashes.SHA256())
        )

def main():
    wallet = Wallet()
    print(f"Wallet: {wallet.__dict__}")
    data = { "foo" : "bar" }
    sig = wallet.gen_signature(data)
    print(f"sig: {sig}")
if __name__ == "__main__":
    main()