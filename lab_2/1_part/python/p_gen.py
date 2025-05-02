import random


try:
    seq = format(random.getrandbits(128), '0128b')
    with open('p_seq.txt', 'w') as f:
        f.write(seq + '\n')
except Exception as e:
    print(f"Error: {e}")
