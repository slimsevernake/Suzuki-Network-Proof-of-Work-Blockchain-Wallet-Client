from backend.utils.hex_to_binary import hex_to_binary

def test_hex_to_binary():
    num = 879
    hex_num = hex(num)[2:]
    binary_num = hex_to_binary(hex_num)

    # It should be a binary int
    assert int(binary_num, 2)