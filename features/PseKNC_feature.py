from utils.statistical_frequence import get_NC_frequency_from_seq
from utils.get_RNAPhyche import get_RNAPhyche
from utils.kmer import get_kmers, kmer2number, number2kmer

import numpy as np


# di_phy_list = ['Rise(RNA)', 'Roll(RNA)', 'Shift(RNA)', 'Slide(RNA)', 'Tilt(RNA)', 'Twist(RNA)', 'Enthalpy(RNA)1',
#                'Entropy(RNA)', 'Stacking_energy(RNA)', 'Free_energy(RNA)']


def get_correlationValue(diPC_df):
    correlationValue = np.zeros((len(diPC_df.columns), len(diPC_df), len(diPC_df)))
    for i in range(len(diPC_df.columns)):
        for j in range(len(diPC_df)):
            for k in range(len(diPC_df)):
                correlationValue[i, j, k] = (diPC_df.iloc[j, i] - diPC_df.iloc[k, i]) ** 2
    return correlationValue


def get_theta_array(seq, lambde, correlationValue):
    theta_array = []
    kmers = get_kmers(seq, 2)
    for ilambda in range(1, lambde + 1):
        theta = 0
        # for i in range(len(seq) - ilambda - 1):
        for i in range(len(seq) - lambde - 1):  # repDNA做法
            pepA = kmers[i]
            pepB = kmers[i + ilambda]

            CC = 0
            for j in range(len(correlationValue)):
                # print(j, pepA, pepB)
                CC += correlationValue[j, pepA, pepB]
                # print(correlationValue[j, pepA, pepB])
            CC /= len(correlationValue)
            theta += CC
        theta_array.append(theta / (len(seq) - ilambda - 1))
    return theta_array


def get_PseDNC_feature(seq, weight, lambde, correlationValue):
    '''
    特征维度为4**2+lambde
    :param seq:
    :param weight:
    :param lambde:
    :return:
    '''
    PseDNC_feature = []
    DNC_frequency = get_NC_frequency_from_seq(seq, k=2)
    theta_array = get_theta_array(seq, lambde, correlationValue=correlationValue)
    for i in range(4 ** 2):
        PseDNC_feature.append(DNC_frequency[i] / (1 + weight * sum(theta_array)))
    for i in range(4 ** 2 + 1, 4 ** 2 + lambde + 1):
        PseDNC_feature.append((weight * theta_array[i - 17]) / (1 + weight * sum(theta_array)))
    return PseDNC_feature


def get_PseKNC_feature(seq, correlationValue, k=3, weight=0.5, lambde=3):
    '''
    特征维度为4**k+lambde
    :param seq:
    :param weight:
    :param lambde:
    :param correlationValue:
    :return:
    '''
    PseKNC_feature = []
    KNC_frequency = get_NC_frequency_from_seq(seq, k=k)
    theta_array = get_theta_array(seq, lambde, correlationValue=correlationValue)
    # print(theta_array)
    for i in range(4 ** k):
        PseKNC_feature.append(KNC_frequency[i] / (1 + weight * sum(theta_array)))
    for i in range(4 ** k + 1, 4 ** k + lambde + 1):
        PseKNC_feature.append((weight * theta_array[i - 4 ** k - 1]) / (1 + weight * sum(theta_array)))
    return PseKNC_feature