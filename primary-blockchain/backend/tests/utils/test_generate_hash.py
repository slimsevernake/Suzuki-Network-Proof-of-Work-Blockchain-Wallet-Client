from backend.utils.generate_hash import generate_hash

def test_generate_hash():
    # It should render proper hash
    assert generate_hash("foo") == "b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b"
    # It should output the same hash given the same arguments in any order
    assert generate_hash(1, [2], "three") == generate_hash("three",1,[2])
