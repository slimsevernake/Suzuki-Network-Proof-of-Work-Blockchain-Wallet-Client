import uuid
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
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
            ec.SECP256K1(), # Koblitz I: prime-generated elliptic curve represented in 256 binary bits
            default_backend()) 
        self.public_key = self.private_key.public_key() # extrapolate pubkey
        self.serialize_public_key()
        
    def gen_signature(self, data):
        """
        Utilizes the local private key to generate a signature for a given input obj,`data`.
        Returns as signature obj, decoded from base into str (serialized).
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode("utf-8"),
            ec.ECDSA(hashes.SHA256()))
        )
    
    def serialize_public_key(self):
        """
        Downgrade/reset public key to serialized form.
        """
        # downgrade to bytes
        self.public_key_as_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        # decode from byte to string
        decoded_public_key = self.public_key_as_bytes.decode("utf-8")
        self.public_key = decoded_public_key

    @staticmethod
    def verify_signature(public_key, data, signature):
        """
        Signature verification.
        Validates a signature against origin pubkey and data object.
        Private method `verify` throws exception as opposed to bool `False`; it 
        is therefore wrapped in a try-catch to produce boolean output.
        """ 

        # deserialize pubkey input
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode("utf-8"),
            default_backend()
        )
        (r, s) = signature
        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s), 
                json.dumps(data).encode("utf-8"),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

def main():
    wallet = Wallet()
    print(f"{wallet.__dict__}")
    data = {"foo": "bar"}
    sig = wallet.gen_signature(data)
    print(f"sig: {sig}")
    valid = Wallet.verify_signature(wallet.public_key, data, sig)
    print(f"valid: {valid}")
    invalid = Wallet.verify_signature(Wallet().public_key, data, sig)
    print(f"invalid: {invalid}")
if __name__ == "__main__":
    main()