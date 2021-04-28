import pandas as pd


class FeatureWrapper:
    def __init__(self):
        self.X = None
        self.Y = None
        self.affliation = None
        self.id = None

    def set_feature_df(self, X, Y, affliation, id):
        '''
        Set the feature_df directly
        :param X: the X of feature_df
        :param Y: the Y of feature_df
        :param affliation: the category of this sample
        :param id: the id of this sample
        :return:
        '''
        if X is not None:
            self.X = X

        # Set labels
        self.Y = Y
        # Set the 'affliation' column as the basis for dividing the training-validation-test set
        self.affliation = affliation
        # Set the 'id' column to identify the data
        self.id = id

    def get_feature_df(self, data_wrapper, feature_func, feature_func_args=None, level='seq', normalize_type=None,
                       feature_name=None):
        '''
        According to the feature function method provided, features are extracted from the data_wrapper.
        :param data_wrapper: data_wrapper
        :param feature_func: feature funtion
        :param feature_func_args: the args of feature funtion
        :param level: if 'seq'，calculate features according to one sequence; if the value is 'df'，calculate features according to the whole dataset.
        :param normalize_type: if the value is None，the data is not standardized; Otherwise, the normalize method is called.
        :return: return feature_df
        '''
        if feature_func_args is None:
            feature_func_args = {}
        if not isinstance(feature_func_args, dict):
            print("Error! feature_func_arg is not q dict.")
            return None

        data_df = data_wrapper.data_df.copy()
        if level == 'seq':
            self.X = data_df['seq'].apply(feature_func, **feature_func_args).apply(pd.Series)
        elif level == 'df':
            self.X = feature_func(data_df, **feature_func_args)
        else:
            print("Error! level must be 'seq' or 'df'")
            return None

        # Add labels
        data_df['Y'] = data_df['label']
        self.Y = data_df['Y']
        # Add an 'id' column to identify the data
        self.id = data_wrapper.data_df['id']
        # Add the 'affliation' column as the basis for dividing the training-validation-test set
        self.affliation = data_wrapper.data_df['affliation']

        if normalize_type is not None:
            self.normalize(normalize_type=normalize_type)

        # Add the names of the feature for each dimension
        if feature_name is not None and feature_name != "":
            columns_len = len(self.X.columns)
            self.X.columns = [feature_name + "_" + str(i) for i in range(columns_len)]

    def save_feature_df_csv(self, csv_path):
        print("save feature_df csv file：" + csv_path)
        self.feature_df.to_csv(csv_path, index=False)

    def add_feature_df(self, data_wrapper, feature_func, feature_func_args=None, level='seq', normalize_type=False,
                       feature_name=None):
        '''
        The new feature is calculated and added after the old feature. The meaning of the parameter is the same as FeatureWrapper.get_feature_df()
        :param data_wrapper:
        :param feature_func:
        :param feature_func_args:
        :param level:
        :param normalize_type:
        :return:
        '''
        if feature_func_args is None:
            feature_func_args = {}

        old_X = self.X
        self.get_feature_df(data_wrapper, feature_func=feature_func, feature_func_args=feature_func_args, level=level,
                            normalize_type=normalize_type, feature_name=feature_name)
        # Combine the old X and new X.
        self.X = pd.concat([old_X, self.X], axis=1)

    def add_X(self, X):
        '''
        Add X to feature_df
        '''
        # Combine the old X and new X.
        self.X = pd.concat([self.X, X], axis=1)

    def normalize(self, normalize_type='respective_standard'):
        '''
        Standardize the self.feature_df.
        Note that if you only want to standardize one feature, please replace it first
        :param normalize_type: The values can be 'respective_standard', 'unify_standard', 'respective_Zscore', and'unify_Zscore'
        :return:
        '''
        train_X = self.train_X
        validate_X = self.validate_X
        test_X = self.test_X
        if normalize_type == 'respective_standard':
            print("The training, validation, test sets are standardized respectively.")
            for col in train_X.columns:
                if train_X.loc[:, col].max() != train_X.loc[:, col].min():
                    train_X.loc[:, col] = (train_X.loc[:, col] - train_X.loc[:, col].min()) / (
                            train_X.loc[:, col].max() - train_X.loc[:, col].min())
            for col in validate_X.columns:
                if validate_X.loc[:, col].max() != validate_X.loc[:, col].min():
                    validate_X.loc[:, col] = (validate_X.loc[:, col] - validate_X.loc[:, col].min()) / (
                            validate_X.loc[:, col].max() - validate_X.loc[:, col].min())
            for col in test_X.columns:
                if test_X.loc[:, col].max() != test_X.loc[:, col].min():
                    test_X.loc[:, col] = (test_X.loc[:, col] - test_X.loc[:, col].min()) / (
                            test_X.loc[:, col].max() - test_X.loc[:, col].min())
        elif normalize_type == 'unify_standard':
            print("The training, validation, and test sets are standardized according to the training set.")
            for col in train_X.columns:  # Note that the training set has to be changed at the end
                if train_X.loc[:, col].max() != train_X.loc[:, col].min():
                    train_X_max = train_X.loc[:, col].max()
                    train_X_min = train_X.loc[:, col].min()
                    validate_X.loc[:, col] = (validate_X.loc[:, col] - train_X_min) / (
                            train_X_max - train_X_min)
                    test_X.loc[:, col] = (test_X.loc[:, col] - train_X_min) / (
                            train_X_max - train_X_min)
                    train_X.loc[:, col] = (train_X.loc[:, col] - train_X_min) / (
                            train_X_max - train_X_min)
                    # print(test_X[col])
        elif normalize_type == 'respective_Zscore':
            print("The Zscore of training, validation, test sets are standardized respectively.")
            for col in train_X.columns:
                if abs(train_X.loc[:, col].std()) > 1e-5:
                    train_X.loc[:, col] = (train_X.loc[:, col] - train_X.loc[:, col].mean()) / (
                        train_X.loc[:, col].std())
            for col in validate_X.columns:
                if abs(validate_X.loc[:, col].std()) > 1e-5:
                    validate_X.loc[:, col] = (validate_X.loc[:, col] - validate_X.loc[:, col].mean()) / (
                        validate_X.loc[:, col].std())
            for col in test_X.columns:
                if abs(test_X.loc[:, col].std()) > 1e-5:
                    test_X.loc[:, col] = (test_X.loc[:, col] - test_X.loc[:, col].mean()) / (test_X.loc[:, col].std())
        elif normalize_type == 'unify_Zscore':
            print("The Zscore of training, validation, and test sets are standardized according to the training set.")
            for col in train_X.columns:
                # print(abs(train_X[col].std()))
                if abs(train_X.loc[:, col].std()) > 1e-5:
                    train_X_mean = train_X.loc[:, col].mean()
                    train_X_std = train_X.loc[:, col].std()
                    validate_X.loc[:, col] = (validate_X.loc[:, col] - train_X_mean) / (train_X_std)
                    test_X.loc[:, col] = (test_X.loc[:, col] - train_X_mean) / (train_X_std)
                    train_X.loc[:, col] = (train_X.loc[:, col] - train_X_mean) / (train_X_std)

        # The training set, validation set, and test set are combined to get self.X
        self.X = pd.concat([train_X, validate_X, test_X])

    def set_sub_feature_indices(self, indices):
        self.X = self.X.loc[:, indices]

    @property
    def train_X(self):
        if self.X is None:
            print("Error! X is None")
        return self.X[self.affliation == 'train']

    @property
    def validate_X(self):
        if self.X is None:
            print("Error! X is None")
        return self.X[self.affliation == 'validate']

    @property
    def test_X(self):
        if self.X is None:
            print("Error! X is None")
        return self.X[self.affliation == 'test']

    @property
    def train_validate_X(self):
        if self.X is None:
            print("Error! X is None")
        if len(self.validate_X) == 0:
            return self.train_X
        else:
            return pd.concat([self.train_X, self.validate_X], axis=0)

    @property
    def train_Y(self):
        if self.Y is None:
            print("Error! X is None")
        return self.Y[self.affliation == 'train']

    @property
    def validate_Y(self):
        if self.Y is None:
            print("Error! X is None")
        return self.Y[self.affliation == 'validate']

    @property
    def test_Y(self):
        if self.Y is None:
            print("Error! X is None")
        return self.Y[self.affliation == 'test']

    @property
    def train_validate_Y(self):
        if self.Y is None:
            print("Error! X is None")
        if len(self.validate_Y) == 0:
            return self.train_Y
        else:
            return pd.concat([self.train_Y, self.validate_Y], axis=0)

    @property
    def feature_df(self):
        return pd.concat([self.X, self.Y, self.affliation, self.id], axis=1)

    @property
    def test_feature_df(self):
        df = pd.concat([self.X, self.Y, self.affliation, self.id], axis=1)
        return df[df.affliation == 'test']
