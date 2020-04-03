import hashlib
import json

def crypto_hash(*args):
    """
    Return SHA256 hash of given args.
    """
    # sort for I/O alignment
    stringified_args = sorted(map(lambda data: json.dumps(data), args)) 
    joined_data = ''.join(stringified_args)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"crypto_hash: {crypto_hash('one', 'two', 3, [4,5])}")
    print(f"crypto_hash: {crypto_hash('two', 'one', 3, [4,5])}")

if __name__=="__main__":
    main()