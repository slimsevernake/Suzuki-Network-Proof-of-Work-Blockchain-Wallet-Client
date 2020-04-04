import hashlib
import json

def generate_hash(*args):
    """
    Return SHA256 hash of given args.
    """
    stringified_args = sorted(map(lambda data: json.dumps(data), args)) # sort for I/O alignment
    joined_data = ''.join(stringified_args)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"generate_hash: {generate_hash('one', 'two', 3, [4,5])}")
    print(f"generate_hash: {generate_hash('two', 'one', 3, [4,5])}")

if __name__=="__main__":
    main()