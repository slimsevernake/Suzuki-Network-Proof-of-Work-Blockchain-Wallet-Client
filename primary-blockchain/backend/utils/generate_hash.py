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
    print(f"noncehash: {generate_hash('2312343431243984', '1934ca6189a119a2086de38e05c1089ae38e05c10fd302e2c11ed2273b234ca9', {'data':'stuff'}, 3,333)}")
    print(f"minihash: {generate_hash('two', 'one', 3, [4,5])}")
# generate_hash(timestamp, prev_hash, data, difficulty, nonce)
if __name__=="__main__":
    main()