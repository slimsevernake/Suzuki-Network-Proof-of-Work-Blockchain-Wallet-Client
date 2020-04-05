import uuid
import time

from backend.wallet.wallet import Wallet

class Transaction:
    """
    Receipt of exchange in network-based currency from sender to one
    or more recipients.
    """
    def __init__(self, sender_wallet, recipient, amount):
        self.id = str(uuid.uuid4())[0:8] 
        self.output = self.generate_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = self.generate_input(
            sender_wallet,
            self.output
        )

    def generate_output(self, sender_wallet, recipient, amount):
        """
        Generates formatted output object to represent Tx data.
        """
        if (amount > sender_wallet.balance):
            raise Exception("Input amount exceeds balance.")

        output = {}
        output[recipient] = amount
        # change
        output[sender_wallet.address] = sender_wallet.balance - amount

        return output

    def generate_input(self, sender_wallet, output):
        """
        Generates formatted input object to represent Tx data.
        Signs Tx, collates sener pubkey + address for further verification.
        """
        return {
            "timestamp": time.time_ns(),
            "amount": sender_wallet.balance,
            "address": sender_wallet.address,
            "public_key": sender_wallet.public_key,
            "signature": sender_wallet.gen_signature(output)
        }

    def tx_update(self, sender_wallet, recipient, amount):
        """
        Update the Tx data object with an existing or new recipient.
        """
        if (amount > self.output[sender_wallet.address]):
            raise Exception("Input amount exceeds balance.")
        # recipient already in output
        if (recipient in self.output):
            self.output[recipient] = self.output[recipient] + amount
        else:
            self.output[recipient] = amount
        # update sender wallet address
        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount
        # re-sign Tx
        self.input = self.generate_input(sender_wallet, self.output)

    @staticmethod
    def is_tx_valid(transaction):
        """
        Determine validity of a transaction.
        """
        output_total  = sum(transaction.output.values())

        if (transaction.input["amount"] != output_total):
            raise Exception("Invalid transaction.")
        
        if not Wallet.verify_signature(
            transaction.input["public_key"],
            transaction.output,
            transaction.input["signature"]
        ): 
            raise Exception("Invalid signature.")

def main():
    tx = Transaction(Wallet(), "recipient", 9)
    print(f"Tx: {tx.__dict__}")

if __name__ == "__main__":
    main()
