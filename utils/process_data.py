from utils.DataWrapper import PersistenceDataWrapper
from utils.data_cleanning import replace_TU

import pandas as pd
from Bio import SeqIO
from sklearn.model_selection import train_test_split


def process_data(pos_train_fa, neg_train_fa, test_fa, shuffle_seed=5, validate_size=None, validate_random_seed=5):
    p_dicts = read_fa(pos_train_fa)
    n_dicts = read_fa(neg_train_fa)
    test_dicts = read_fa(test_fa)
    P_df = seq_dicts2df(p_dicts, label='P')
    N_df = seq_dicts2df(n_dicts, label='N')
    test_df = seq_dicts2df(test_dicts, label='U')
    train_validate_df = pd.concat([P_df, N_df], axis=0)

    if shuffle_seed is not None:
        # Shuffule the training set data.
        from sklearn.utils import shuffle
        train_validate_df = shuffle(train_validate_df, random_state=shuffle_seed)

    # Spilt the training and validation set.
    if validate_size is not None and validate_size > 0.:
        train_df, validate_df = train_test_split(train_validate_df, random_state=validate_random_seed, shuffle=True,
                                                 test_size=validate_size)
    else:
        train_df = train_validate_df
        validate_df = None

    data_wrapper = PersistenceDataWrapper(train_data_df=train_df, validate_data_df=validate_df, test_data_df=test_df)
    data_wrapper = replace_TU(data_wrapper)  # replace 'T' with 'U' in the sequence
    return data_wrapper


def read_fa(path):
    records = list(SeqIO.parse(path, format="fasta"))
    id_seq_dict = {}
    for x in records:
        id = str(x.id)
        seq = "".join([x for x in str(x.seq).replace("U", "T") if x in "ATCG"])
        id_seq_dict[id] = seq
    return id_seq_dict


def seq_dicts2df(seq_dicts, label):
    df = pd.DataFrame()
    df['id'] = list(seq_dicts.keys())
    df['seq'] = list(seq_dicts.values())
    df['label'] = [label for i in range(len(seq_dicts))]
    return df


if __name__ == "__main__":
    pos_train_fa = "../datasets/A101/A101_Train_P.fasta"
    neg_train_fa = "../datasets/A101/A101_Train_N.fasta"
    test_fa = "../datasets/A101/A101_Test.fasta"
    datawrapper = process_data(pos_train_fa, neg_train_fa, test_fa)
    print(datawrapper.data_df)
