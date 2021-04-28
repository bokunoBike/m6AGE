import numpy as np
import pandas as pd

dataframe_columns = ["id", "seq", "label"]  # The names of columns


class DataWrapper:
    def __init__(self, data_df=None, tvt_size=np.array([0.6, 0.2, 0.2]), csv_path=""):
        '''
        :param data_df: The dataframe
        :param tvt_size: The ratio of training-validation-test set. Where tvt_size[0] represents training set，tvt_size[1] represents validation set，tvt_size[2] represents test set，and the sum of the three is 1.
        :param csv_path: if data_df is None，then import the data from the path of the CSV file。
        '''
        # read dataframe
        if data_df is not None:
            self.data_df = data_df
        elif csv_path != "":
            self.data_df = pd.read_csv(csv_path)
        else:
            print("Error! data_df is None")
            return

        self.data_df = self.data_df[dataframe_columns]  # read the specific columns

        self.data_df['affliation'] = 'Unkown'  # add 'affliztion' column
        self.data_df['label'] = self.data_df['label'].map({'P': 1, 'N': 0, 1: 1, 0: 0, '1': 1, '0': 0, 'U': -2})

        # Split traning-validation-test set
        self.divide_tvt(tvt_size)

    def divide_tvt(self, tvt_size):
        '''
        Split traning-validation-test set
        :param tvt_size: The ratio of training-validation-test set. Where tvt_size[0] represents training set，tvt_size[1] represents validation set，tvt_size[2] represents test set，and the sum of the three is 1. If tvt_size is None, use the init tvt_size.
        :return:
        '''
        tvt_size = np.array(tvt_size)
        tvt_size = tvt_size / tvt_size.sum()  # normalize
        print("set the tvt_size as" + str(tvt_size), sep=' ')
        self.tvt_size = tvt_size

        affliation = [i for i in range(len(self.data_df))]
        train_division = affliation[: int(self.tvt_size[0] * len(affliation))]
        validate_division = affliation[int(self.tvt_size[0] * len(affliation)): int(
            (self.tvt_size[0] + self.tvt_size[1]) * len(affliation))]
        test_division = affliation[int(
            (self.tvt_size[0] + self.tvt_size[1]) * len(affliation)):]

        for i in train_division:
            affliation[i] = 0
        for i in validate_division:
            affliation[i] = 1
        for i in test_division:
            affliation[i] = 2
        # split traning-validation-test set
        self.data_df['affliation'] = affliation
        self.data_df['affliation'] = self.data_df['affliation'].map({0: 'train', 1: 'validate', 2: 'test'})

    @property
    def train_data_df(self):
        return self.data_df[self.data_df.affliation == 'train']

    @property
    def validate_data_df(self):
        return self.data_df[self.data_df.affliation == 'validate']

    @property
    def test_data_df(self):
        return self.data_df[self.data_df.affliation == 'test']

    @property
    def train_label(self):
        return self.train_data_df['label']

    @property
    def validate_label(self):
        return self.validate_data_df['label']

    @property
    def test_label(self):
        return self.test_data_df['label']

    @property
    def label(self):
        return self.data_df['label']


# It is suitable for the case that the training set and the test set have been divided
class PersistenceDataWrapper(DataWrapper):
    def __init__(self, train_data_df=None, test_data_df=None, validate_data_df=None, train_csv_path=None,
                 test_csv_path="", validate_csv_path=""):
        self.test_size = None

        # init train_data_df
        if train_data_df is not None:
            pass
        elif train_csv_path != "":
            train_data_df = pd.read_csv(train_csv_path)
        if train_data_df is None:
            print("Error! train_data_df is None")
            return
        train_data_df = train_data_df[dataframe_columns]
        train_data_df['affliation'] = 'train'

        # init test_data_df
        if test_data_df is not None:
            pass
        elif test_csv_path != "":
            test_data_df = pd.read_csv(test_csv_path)
        if test_data_df is None:
            print("Error! train_data_df is None.")
            return
        test_data_df = test_data_df[dataframe_columns]
        test_data_df['affliation'] = 'test'

        # init validate_data_df
        if validate_data_df is not None:
            pass
        elif validate_csv_path != "":
            validate_data_df = pd.read_csv(validate_csv_path)
        if validate_data_df is None:
            print("No validation set.")
        else:
            validate_data_df = validate_data_df[dataframe_columns]
            validate_data_df['affliation'] = 'validate'

        # merge
        if validate_data_df is None:
            self.data_df = pd.concat([train_data_df, test_data_df], ignore_index=True)
        else:
            self.data_df = pd.concat([train_data_df, validate_data_df, test_data_df], ignore_index=True)
        self.data_df['label'] = self.data_df['label'].map({'P': 1, 'N': 0, 1: 1, 0: 0, '1': 1, '0': 0, 'U': -2})

        # calculate tvt_size
        if validate_data_df is None:
            test_size = len(test_data_df) / (len(train_data_df) + len(test_data_df))
            self.tvt_size = np.array([1 - test_size, 0, test_size])
        else:
            test_size = len(test_data_df) / (len(train_data_df) + len(test_data_df) + len(validate_data_df))
            validate_size = len(validate_data_df) / (len(train_data_df) + len(test_data_df) + len(validate_data_df))
            self.tvt_size = np.array([1 - test_size - validate_size, validate_size, test_size])