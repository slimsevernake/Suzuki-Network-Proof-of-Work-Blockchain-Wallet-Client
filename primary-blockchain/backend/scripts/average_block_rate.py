from sys import argv
import time 
from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS
"""
A simple script which determines the average block production rate given
an input Blockchain instance running for n iterations, a user-elicited integer
"""

blockchain = Blockchain()

times = []
iterations = int(argv[1])
for i in range(iterations):
    start_time = time.time_ns()
    blockchain.add_block(i)
    end_time = time.time_ns()

    time_to_mine = (end_time - start_time) / SECONDS
    times.append(time_to_mine)

    average_time = sum(times) / len(times)

    print(f"""
    Iteration: {i}
    New block difficulty: {blockchain.chain[-1].difficulty}
    print(f"Time to mine new block: {time_to_mine}s
    print(f"Average time to add blocks: {average_time}s\n""")


