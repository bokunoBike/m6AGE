# source：SRAMP Nucleotide pair spectrum encoding (spectrum encoding)
import numpy as np

d_max = 3

bn_dict = {('A', 'A'): 0, ('A', 'U'): 1, ('A', 'C'): 2, ('A', 'G'): 3, ('U', 'A'): 4, ('U', 'U'): 5, ('U', 'C'): 6,
           ('U', 'G'): 7, ('C', 'A'): 8, ('C', 'U'): 9, ('C', 'C'): 10, ('C', 'G'): 11, ('G', 'A'): 12, ('G', 'U'): 13,
           ('G', 'C'): 14, ('G', 'G'): 15}


def get_NPS_features(seq):
    res = []
    seq_len = len(seq)
    if seq_len < d_max + 2:
        print("error")
        return None
    for d in range(d_max + 1):
        pair_count = np.zeros(16)
        for i in range(seq_len - 1 - d):
            index = bn_dict[(seq[i], seq[i + d + 1])]
            pair_count[index] += 1
        res.extend(pair_count / (seq_len - d - 1))
    return res


if __name__ == "__main__":
    a = get_NPS_features("GAACCAUUAGA")
    print(len(a))
    print(a)
