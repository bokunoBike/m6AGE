def get_pos_neg_subsets_df(df):  # Gets a positive samples subset and negative samples subset in the DataFrame
    positive_subsets_df = df[df.label == 1]
    negative_subsets_df = df[df.label == 0]
    if len(positive_subsets_df) == 0:
        positive_subsets_df = df[df.label == 'P']
    if len(negative_subsets_df) == 0:
        negative_subsets_df = df[df.label == 'N']
    return positive_subsets_df, negative_subsets_df
