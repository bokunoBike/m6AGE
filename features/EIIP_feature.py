# Nair (8) came up with electron-ion interaction pseudopotentials (EIIP) value of nucleotides A, G, C, T (A: 0.1260, C: 0.1340, G: 0.0806, T:0.1335). The EIIP directly use the EIIP value represent the nucleotide in the DNA sequence. Therefore, the dimension of the EIIP descriptor is the length of the DNA sequence.
from utils.kmer import number2kmer
from utils.statistical_frequence import get_NC_frequency_from_seq

EIIP_dict = {'A': 0.1260, 'C': 0.1340, 'G': 0.0806, 'U': 0.1335, 'T': 0.1335}
PseEIIP_list = list()
for i in range(4 ** 3):
    tn = number2kmer(i, k=3)
    PseEIIP_list.append(EIIP_dict[tn[0]] + EIIP_dict[tn[1]] + EIIP_dict[tn[2]])


def get_EIIP_feature(seq):
    EIIP_feature = list()
    for n in seq:
        EIIP_feature.append(EIIP_dict[n])
    return EIIP_feature


def get_PseEIIP_feature(seq):
    NC_frequency = get_NC_frequency_from_seq(seq, k=3, type='list')
    # print(len(PseEIIP_list))
    # print(len(NC_frequency))
    PseEIIP_feature = list(map(lambda x, y: x * y, NC_frequency, PseEIIP_list))
    return PseEIIP_feature
