from backend.utils.generate_hash import generate_hash

HEX_TO_BINARY_CONVERSION_TABLE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "a": "1010",
    "b": "1011",
    "c": "1100", 
    "d": "1101", 
    "e": "1110",
    "f": "1111"
}

def hex_to_binary(hex_string):
    binary_string = ""
    
    for char in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[char]
    
    return binary_string

def main():
    num = 451
    hexnum = hex(num)[2:]
    print(f"hexnum: {hexnum}")

    binarynum = hex_to_binary(hexnum)
    print(f"binarynum: {binarynum}")

    original_num = int(binarynum, 2)
    print(f"original_num: {original_num}")

    hex_to_binary_generate_hash = hex_to_binary(generate_hash("test_data"))
    print(f"hex_to_binary_generate_hash: {hex_to_binary_generate_hash}")
    
if __name__=="__main__":
    main()
