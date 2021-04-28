# 核苷酸对位置特异性（NPPS）
# Identifying N6-methyladenosine sites using multi-interval nucleotide pair position specificity and support vector machine

from utils.statistical_frequence import get_dinuc_with_interval_postion_frequency, get_kmer_position_frequency
from utils.common_functions import get_pos_neg_subsets_df
from utils.kmer import kmer2number, get_dinucNum_with_interval, number2kmer
import numpy as np


def get_NPPS_feature(seq, xi, pos_front_Tp, pos_post_Tp, neg_front_Tp, neg_post_Tp):
    NPPS_feature = []
    dinucNums = get_dinucNum_with_interval(seq, xi=xi)
    for i, dinucNum in zip(range(len(dinucNums)), dinucNums):
        # NPPS_feature.append(pos_front_Tp[dinucNum][i])
        # NPPS_feature.append(pos_post_Tp[dinucNum][i])
        # NPPS_feature.append(neg_front_Tp[dinucNum][i])
        # NPPS_feature.append(neg_post_Tp[dinucNum][i])
        NPPS_feature.append(pos_post_Tp[dinucNum][i] - neg_post_Tp[dinucNum][i])
    # print(NPPS_feature)
    return NPPS_feature


def get_front_post_Tp(df, xi):
    Ts = get_kmer_position_frequency(df, k=1)
    Td = get_dinuc_with_interval_postion_frequency(df, xi=xi)
    front_Tp = np.zeros(Td.shape)
    post_Tp = np.zeros(Td.shape)
    for i in range(front_Tp.shape[0]):
        for j in range(front_Tp.shape[1]):
            if Ts[int(i / 4)][j] == 0:
                front_Tp[i][j] = 0.
            else:
                front_Tp[i][j] = Td[i][j] / Ts[int(i / 4)][j]
            if Ts[int(i / 4)][j + xi + 1] == 0:
                post_Tp[i][j] = 0.
            else:
                post_Tp[i][j] = Td[i][j] / Ts[int(i / 4)][j + xi + 1]
    return front_Tp, post_Tp


def get_pos_neg_front_post_Tp(train_data_df, xi):
    positive_subsets_df, negative_subsets_df = get_pos_neg_subsets_df(train_data_df)
    pos_front_Tp, pos_post_Tp = get_front_post_Tp(positive_subsets_df, xi=xi)
    neg_front_Tp, neg_post_Tp = get_front_post_Tp(negative_subsets_df, xi=xi)
    return pos_front_Tp, pos_post_Tp, neg_front_Tp, neg_post_Tp
