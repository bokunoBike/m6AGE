from utils.kmer import get_kmers, number2kmer, get_dinucNum_with_interval
from collections import Counter
import numpy as np
import pandas as pd


def get_kmer_position_frequency(df, k):
    seq_df = df['seq'].apply(get_kmers, k=k).apply(pd.Series)
    position_frequency = np.zeros((4 ** k, seq_df.columns.size))
    for col in seq_df.columns:
        # print(col)
        kmer_p = seq_df[col].value_counts(normalize=True)  # 某个位置的kmer的出现频率
        for kmerN, p in zip(kmer_p.index, kmer_p):
            # print(nuc, p)
            position_frequency[int(kmerN)][col] = p
    return position_frequency


def get_dinuc_with_interval_postion_frequency(df, xi):
    seq_df = df['seq'].apply(get_dinucNum_with_interval, xi=xi).apply(pd.Series)
    position_frequency = np.zeros((4 ** 2, seq_df.columns.size))
    for col in seq_df.columns:
        kmer_p = seq_df[col].value_counts(normalize=True)  # 某个位置的kmer出现的频率
        for kmerN, p in zip(kmer_p.index, kmer_p):
            # print(nuc, p)
            # print(kmerN, p, col)
            position_frequency[int(kmerN)][col] = p
    return position_frequency


def get_NC_frequency_from_seq(seq, k, type='list'):
    '''
    The frequency of kmers is counted from the sequence.
    :param seq: input sequence
    :param k:
    :param type: if the value is "list"，then return a list of frequency according to the kmerNumber; else return a dict.
    :return:
    '''
    if type != 'list' and type != 'dict':
        print("error! Return normalize_type must be list or dict")

    counter = Counter(get_kmers(seq, k))
    frequence_list = [0 for i in range(4 ** k)]
    for key in counter.keys():
        frequence_list[key] += counter[key]
    frequence_list = list(np.array(frequence_list) / np.array(frequence_list).sum())
    if type == 'list':
        return frequence_list
    else:
        frequence_dict = dict()
        for i in range(4 ** k):
            frequence_dict[number2kmer(i, k=k)] = frequence_list[i]
        return frequence_dict


def get_NC_frequence_from_seq(seq, k, type='list'):  # 从seq中统计kmer的频数
    if type != 'list' and type != 'dict':
        print("error! Return normalize_type must be list or dict")

    counter = Counter(get_kmers(seq, k))
    frequence_list = [0 for i in range(4 ** k)]
    for key in counter.keys():
        frequence_list[key] += counter[key]
    if type == 'list':
        return frequence_list
    else:
        frequence_dict = dict()
        for i in range(4 ** k):
            frequence_dict[number2kmer(i, k=k)] = frequence_list[i]
        return frequence_dict


def get_NC_frequency_from_df(df, k, type='list'):  # 从dataframe中统计kmer的频率
    if type != 'list' and type != 'dict':
        print("error! Return normalize_type must be list or dict")

    frequence_list = [0 for i in range(4 ** k)]

    def statistic(seq_frequence_list, frequence_list):
        for i in range(len(seq_frequence_list)):
            frequence_list[i] += seq_frequence_list[i]

    df['seq'].apply(get_NC_frequence_from_seq, k=k).apply(statistic, frequence_list=frequence_list)
    frequency_list = list(np.array(frequence_list) / np.array(frequence_list).sum())
    # print("frequency_list", frequency_list)
    if type == 'list':
        return frequency_list
    else:
        frequency_dict = dict()
        for i in range(4 ** k):
            frequency_dict[number2kmer(i, k=k)] = frequency_list[i]
        return frequency_dict


if __name__ == "__main__":
    seq = "GAUGAAGCUAUAGCUGAUAAUGAGCUAACGGAGGAGACCAAAAAAGGAAAACAUUCUCCUGUUGCAAAAUUGGUGGAACAACCUGGCGAGCCUGCAAAAGA"
    print(get_NC_frequency_from_seq(seq, 2, type='list'))
