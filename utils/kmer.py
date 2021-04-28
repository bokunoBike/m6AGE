# Define some operations related to "kmer"

from utils.nucleotide_number import nuc2num_dict, num2nuc_dict


def get_kmers(seq, k):  # extract kmers according to the order of the the sequence
    kmers = []
    tmp = 0
    for i in range(k - 1):
        tmp += nuc2num_dict[seq[i]] * (4 ** (k - i - 2))

    for i in range(len(seq) - k + 1):
        tmp = tmp % (4 ** (k - 1)) * 4 + nuc2num_dict[seq[i + k - 1]]
        kmers.append(tmp)
    return kmers


def kmer2number(kmer):  # Convert kmer to corresponding number，for example, 'AAG' -> 2
    k = len(kmer)
    res = 0
    for i in range(k):
        res += nuc2num_dict[kmer[i]] * (4 ** (k - i - 1))
    return res


def number2kmer(num, k=0):  # Convert the number to corresponding kmer，for example, 2 -> 'G'(k=0), or 2 -> 'AAG'(k=3)
    kmer_list = []
    while num != 0:
        remainder = num % 4
        num = int(num / 4)
        kmer_list.insert(0, num2nuc_dict[remainder])
    if k != 0:
        if k >= len(kmer_list):
            for i in range(k - len(kmer_list)):
                kmer_list.insert(0, 'A')
        else:
            print("error! k is less than the length of kmer_list.")
    return "".join(kmer_list)


def get_dinucNum_with_interval(seq, xi=0):  # xi is the interval length, and the function returns the array list
    dinucNum = []
    subseqs = [seq[i::xi + 1] for i in range(xi + 1)]
    # print(subseqs)
    subseq_dinucNums = [get_kmers(subseq, 2) for subseq in subseqs]

    for subseq_dinucNum in subseq_dinucNums:
        if len(subseq_dinucNum) < len(subseq_dinucNums[0]):
            subseq_dinucNum.append(None)
    for i in zip(*subseq_dinucNums):
        dinucNum.extend(list(i))
    dinucNum = list(filter(lambda a: a is not None, dinucNum))
    return dinucNum


if __name__ == "__main__":
    # num = 2
    # k = 3
    # print(number2kmer(num, k))
    #
    # xi = 0
    # seq = "AUUCGGCACG"
    # seq = "GAGUAAAUCCAGUAAUGGUCUGGUUUGGUACUUAUUCUUAGUGUCUAUAAACAUUUCUUAGUUUCUCUUGCCUAUUUGCAUUUCAAUUUCACUUGGUACAA"
    # dinucNums = get_dinucNum_with_interval(seq, xi)
    # print(len(dinucNums))
    # for dinuc in dinucNums:
    #     print(int(dinuc / 4))
    for i in range(64):
        print(number2kmer(i, 3))
