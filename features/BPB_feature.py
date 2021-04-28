# Bi-proﬁle Bayes
# Paper source : RNA-MethylPred: A high-accuracy predictor to identify N6-methyladenosine in RNA

from utils.statistical_frequence import get_kmer_position_frequency
from utils.nucleotide_number import nuc2num_dict
from utils.common_functions import get_pos_neg_subsets_df


def get_pos_neg_posteriori_probability(train_data_df):  # 获取训练集中正例和负例的kmer在各个位置上的后验概率
    positive_subsets_df, negative_subsets_df = get_pos_neg_subsets_df(train_data_df)

    positive_posteriori_probability = get_kmer_position_frequency(positive_subsets_df, k=1)
    negative_posteriori_probability = get_kmer_position_frequency(negative_subsets_df, k=1)
    return positive_posteriori_probability, negative_posteriori_probability


def get_BPB_feature(seq, positive_posteriori_probability, negative_posteriori_probability):
    BPB_feature = []
    if 'N' in seq:
        print("error! The N can't in seq.")
    if len(seq) != positive_posteriori_probability.shape[1] or len(seq) != negative_posteriori_probability.shape[1]:
        print(
            "error! The length of seq is not equal to positive_posteriori_probability or negative_posteriori_probability.")
    for i in range(len(seq)):
        BPB_feature.append(positive_posteriori_probability[nuc2num_dict[seq[i]]][i])
        BPB_feature.append(negative_posteriori_probability[nuc2num_dict[seq[i]]][i])
    return BPB_feature
