import pandas as pd

from utils.process_data import process_data
from utils.FeatureWrapper import FeatureWrapper
from features.get_node_embeddings import get_node_embeddings
from models.CatBoost_Model import CatBoost_Model


def train_and_test(pos_train_fa, neg_train_fa, test_fa, dataset, out_path, save_path=None):
    data_wrapper = process_data(pos_train_fa, neg_train_fa, test_fa)
    print("get_data_wrapper")
    feature_wrapper = get_features(data_wrapper, dataset=dataset, save_path=save_path)
    print("get_feature_wrapper")
    print(feature_wrapper.train_X)
    print(feature_wrapper.train_Y)
    make_prediction(feature_wrapper=feature_wrapper, dataset=dataset, out_path=out_path)
    print("get_results")


def get_features(data_wrapper, dataset, save_path=None):
    from parameters import dataset_parameters_dict

    seq_features_list = dataset_parameters_dict[dataset]["features"]
    neighbor_num = dataset_parameters_dict[dataset]["neighbor_num"]
    ne_methods_dict = dataset_parameters_dict[dataset]["embeddings"]
    if seq_features_list is None or seq_features_list == []:
        seq_features_list = select_features(data_wrapper=data_wrapper, dataset=dataset)
    feature_wrapper = get_seq_features(datawrapper=data_wrapper, seq_features_list=seq_features_list)
    from features.get_node_embeddings import get_Graph, get_Graph2
    if dataset == "A101":
        G = get_Graph(feature_wrapper.X, neighbor_num=neighbor_num)
    else:
        G = get_Graph2(feature_wrapper.X, neighbor_num=neighbor_num)
    node_embeddings_df = get_node_embeddings(feature_wrapper.X, G, ne_methods_dict=ne_methods_dict)
    node_embeddings_df.columns = ["GraphEmbeddings_" + str(i) for i in range(len(node_embeddings_df.columns))]

    feature_wrapper.add_X(node_embeddings_df)
    if save_path is not None:  # save the features to the file
        feature_wrapper.save_feature_df_csv(save_path)
    return feature_wrapper


def select_features(data_wrapper, dataset, reference_number=20):
    print("start select features")
    from parameters import dataset_parameters_dict
    model_func_args = dataset_parameters_dict[dataset]["catboost"]
    model = CatBoost_Model()
    all_feature_list = ["BPB", "NPPS-xi3", "NPPS-xi2", "NPPS-xi1", "NPS", "CTD", "PseKNC", "NCP-ND", "EIIP"]
    feature_wrapper = get_seq_features(data_wrapper, all_feature_list)
    model.train(train_X=feature_wrapper.train_X, train_Y=feature_wrapper.train_Y, **model_func_args)
    importances = model.model.feature_importances_
    names = model.model.feature_names_
    x = [(name, importance) for name, importance in zip(names, importances)]
    x = sorted(x, key=lambda k: -k[1])[:reference_number]
    select_feature_list = []
    for item in x:
        name = item[0].split("_")[0]
        if name not in select_feature_list:
            select_feature_list.append(name)
    print("select feature_list", select_feature_list)
    return select_feature_list


def make_prediction(feature_wrapper, dataset, out_path):
    from parameters import dataset_parameters_dict
    model_func_args = dataset_parameters_dict[dataset]["catboost"]
    model = CatBoost_Model()
    print("start training")
    print(model_func_args)
    y_pred, y_score = model.train_predict_pred_score(train_X=feature_wrapper.train_X, train_Y=feature_wrapper.train_Y,
                                                     test_X=feature_wrapper.test_X, model_func_args=model_func_args)

    result_df = pd.DataFrame()
    result_df['id'] = feature_wrapper.test_feature_df['id']
    result_df['y_pred'] = y_pred
    result_df['y_score'] = y_score
    result_df.to_csv(out_path, index=False)


def get_seq_features(datawrapper, seq_features_list) -> FeatureWrapper:
    # 构建序列特征
    from features.BPB_feature import get_pos_neg_posteriori_probability, get_BPB_feature
    from features.NPS_feature import get_NPS_features
    from features.CTD_feature import get_CTD_feature
    from features.NPPS_feature import get_pos_neg_front_post_Tp, get_NPPS_feature
    from features.PseKNC_feature import get_RNAPhyche, get_correlationValue, kmer2number, get_PseKNC_feature
    from features.NCP_ND_feature import get_NCP_ND_feature
    from features.EIIP_feature import get_EIIP_feature, get_PseEIIP_feature

    feature_wrapper = FeatureWrapper()

    for use_seq_feature in seq_features_list:
        if use_seq_feature == "BPB":
            positive_posteriori_probability, negative_posteriori_probability = get_pos_neg_posteriori_probability(
                datawrapper.train_data_df)

            feature_wrapper.add_feature_df(datawrapper, feature_func=get_BPB_feature, feature_func_args={
                "positive_posteriori_probability": positive_posteriori_probability,
                "negative_posteriori_probability": negative_posteriori_probability}, feature_name=use_seq_feature)

        elif use_seq_feature == "NPPS-xi3":
            xi = 3
            pos_front_Tp, pos_post_Tp, neg_front_Tp, neg_post_Tp = get_pos_neg_front_post_Tp(datawrapper.train_data_df,
                                                                                             xi=xi)

            feature_wrapper.add_feature_df(datawrapper, feature_func=get_NPPS_feature,
                                           feature_func_args={'xi': xi, 'pos_front_Tp': pos_front_Tp,
                                                              'pos_post_Tp': pos_post_Tp,
                                                              'neg_front_Tp': neg_front_Tp,
                                                              'neg_post_Tp': neg_post_Tp, },
                                           feature_name=use_seq_feature)

        elif use_seq_feature == "NPPS-xi2":
            xi = 2
            pos_front_Tp, pos_post_Tp, neg_front_Tp, neg_post_Tp = get_pos_neg_front_post_Tp(datawrapper.train_data_df,
                                                                                             xi=xi)

            feature_wrapper.add_feature_df(datawrapper, feature_func=get_NPPS_feature,
                                           feature_func_args={'xi': xi, 'pos_front_Tp': pos_front_Tp,
                                                              'pos_post_Tp': pos_post_Tp,
                                                              'neg_front_Tp': neg_front_Tp,
                                                              'neg_post_Tp': neg_post_Tp, },
                                           feature_name=use_seq_feature)

        elif use_seq_feature == "NPPS-xi1":
            xi = 1
            pos_front_Tp, pos_post_Tp, neg_front_Tp, neg_post_Tp = get_pos_neg_front_post_Tp(datawrapper.train_data_df,
                                                                                             xi=xi)

            feature_wrapper.add_feature_df(datawrapper, feature_func=get_NPPS_feature,
                                           feature_func_args={'xi': xi, 'pos_front_Tp': pos_front_Tp,
                                                              'pos_post_Tp': pos_post_Tp,
                                                              'neg_front_Tp': neg_front_Tp,
                                                              'neg_post_Tp': neg_post_Tp, },
                                           feature_name=use_seq_feature)

        elif use_seq_feature == "NPS":
            feature_wrapper.add_feature_df(datawrapper, feature_func=get_NPS_features, feature_name=use_seq_feature)
        # print(len(feature_wrapper.X.columns))

        elif use_seq_feature == "CTD":
            feature_wrapper.add_feature_df(datawrapper, feature_func=get_CTD_feature, feature_name=use_seq_feature)
            # # print(len(feature_wrapper.X.columns))


        elif use_seq_feature == "PseKNC":
            di_phy_list = ['Rise(RNA)', 'Roll(RNA)', 'Shift(RNA)', 'Slide(RNA)', 'Tilt(RNA)', 'Twist(RNA)']
            diPC_df = get_RNAPhyche(phy_list=di_phy_list, k=2, standardized=False)
            diPC_df['kmer'] = diPC_df.index
            diPC_df['kmer'] = diPC_df['kmer'].apply(kmer2number)
            diPC_df = diPC_df.set_index('kmer')
            # print(diPC_df)

            correlationValue = get_correlationValue(diPC_df)
            k = 3
            feature_wrapper.add_feature_df(datawrapper, get_PseKNC_feature,
                                           feature_func_args={"k": k, "correlationValue": correlationValue},
                                           feature_name=use_seq_feature)
        elif use_seq_feature == "NCP-ND":
            feature_wrapper.add_feature_df(datawrapper, feature_func=get_NCP_ND_feature, feature_name=use_seq_feature)

        elif use_seq_feature == "EIIP":
            feature_wrapper.add_feature_df(datawrapper, feature_func=get_EIIP_feature, feature_name=use_seq_feature)

        else:
            print("error!")
            return
    return feature_wrapper
