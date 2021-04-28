import numpy as np
import pandas as pd
import networkx as nx


def get_LNS(feature_matrix, neighbor_num):
    feature_matrix = np.matrix(feature_matrix)
    iteration_max = 40  # same as 2018 bibm
    mu = 3  # same as 2018 bibm
    X = feature_matrix
    alpha = np.power(X, 2).sum(axis=1)
    distance_matrix = np.sqrt(alpha + alpha.T - 2 * X * X.T)
    row_num = X.shape[0]
    e = np.ones((row_num, 1))
    distance_matrix = np.array(distance_matrix + np.diag(np.diag(e * e.T * np.inf)))
    sort_index = np.argsort(distance_matrix, kind='mergesort')
    nearest_neighbor_index = sort_index[:, :neighbor_num].flatten()
    nearest_neighbor_matrix = np.zeros((row_num, row_num))
    nearest_neighbor_matrix[np.arange(row_num).repeat(neighbor_num), nearest_neighbor_index] = 1
    C = nearest_neighbor_matrix
    np.random.seed(0)
    W = np.mat(np.random.rand(row_num, row_num), dtype=float)
    W = np.multiply(C, W)
    lamda = mu * e
    P = X * X.T + lamda * e.T
    for q in range(iteration_max):
        Q = W * P
        W = np.multiply(W, P) / Q
        W = np.nan_to_num(W)
    return np.array(W)


def get_Graph(df, neighbor_num=20):
    print("neighbor_num=", neighbor_num)
    # 获取Graph
    feature_matrix = list(df.values)
    p_n_fs_w = get_LNS((np.array(feature_matrix)), neighbor_num=neighbor_num)
    p_n_fs_w_df = pd.DataFrame(p_n_fs_w, columns=list(range(len(df))),
                               index=list(range(len(df))))
    # print(p_n_fs_w_df)

    G = nx.from_pandas_adjacency(p_n_fs_w_df, create_using=nx.Graph())
    if not nx.is_connected(G):
        print("Error! The initial graph is not connected.")
    t = 0.9
    print("get Graph")
    p_n_fs_w_df_new = p_n_fs_w_df
    p_n_fs_w_df_new[p_n_fs_w_df > t] = 1
    p_n_fs_w_df_new[p_n_fs_w_df <= t] = 0
    # G = nx.from_pandas_adjacency(p_n_fs_w_df_new, create_using=nx.Graph())
    while not nx.is_connected(G):
        p_n_fs_w_df_new = p_n_fs_w_df
        t = t - 0.001
        p_n_fs_w_df_new[p_n_fs_w_df > t] = 1
        p_n_fs_w_df_new[p_n_fs_w_df <= t] = 0
        G = nx.from_pandas_adjacency(p_n_fs_w_df_new, create_using=nx.Graph())
    # print(p_n_fs_w_df_new)
    print("G is connected", nx.is_connected(G))
    return G


def get_Graph2(df, neighbor_num=20, init_t=None):
    print("neighbor_num =", neighbor_num)
    feature_matrix = list(df.values)
    p_n_fs_w = get_LNS((np.array(feature_matrix)), neighbor_num=neighbor_num)
    p_n_fs_w_df = pd.DataFrame(p_n_fs_w, columns=list(range(len(df))),
                               index=list(range(len(df))))
    # print(p_n_fs_w_df)

    # 判断初始Graph是否是连通图，若不是，则增加neighbor_num，直到G为连通图
    G = nx.from_pandas_adjacency(p_n_fs_w_df, create_using=nx.Graph())
    while not nx.is_connected(G):
        neighbor_num += 10
        print("neighbor_num is added to", neighbor_num)
        p_n_fs_w = get_LNS((np.array(feature_matrix)), neighbor_num=neighbor_num)
        p_n_fs_w_df = pd.DataFrame(p_n_fs_w, columns=list(range(len(df))),
                                   index=list(range(len(df))))
        G = nx.from_pandas_adjacency(p_n_fs_w_df, create_using=nx.Graph())

    t = 1 / neighbor_num
    if init_t is not None:
        t = init_t
    print("get Graph")
    p_n_fs_w_df_new = p_n_fs_w_df.copy()
    p_n_fs_w_df_new[p_n_fs_w_df > t] = 1
    p_n_fs_w_df_new[p_n_fs_w_df <= t] = 0
    G = nx.from_pandas_adjacency(p_n_fs_w_df_new, create_using=nx.Graph())

    while not nx.is_connected(G):
        p_n_fs_w_df_new = p_n_fs_w_df.copy()
        t = t - 1 / (neighbor_num * 100)
        p_n_fs_w_df_new[p_n_fs_w_df > t] = 1
        p_n_fs_w_df_new[p_n_fs_w_df <= t] = 0
        G = nx.from_pandas_adjacency(p_n_fs_w_df_new, create_using=nx.Graph())
    # print(p_n_fs_w_df_new)
    print("The threshold value ", t)
    print("G is connected", nx.is_connected(G))
    return G


def get_Graph3(df, neighbor_num=20, init_t=None):
    print("neighbor_num=", neighbor_num)
    feature_matrix = list(df.values)
    p_n_fs_w = get_LNS((np.array(feature_matrix)), neighbor_num=neighbor_num)
    p_n_fs_w_df = pd.DataFrame(p_n_fs_w, columns=list(range(len(df))),
                               index=list(range(len(df))))
    # print(p_n_fs_w_df)

    t = 1 / neighbor_num
    if init_t is not None:
        t = init_t
    print("get Graph")
    p_n_fs_w_df_new = p_n_fs_w_df.copy()
    p_n_fs_w_df_new[p_n_fs_w_df <= t] = 0
    G = nx.from_pandas_adjacency(p_n_fs_w_df_new, create_using=nx.Graph())

    while not nx.is_connected(G):
        p_n_fs_w_df_new = p_n_fs_w_df.copy()
        t = t - 1 / (neighbor_num * 100)
        p_n_fs_w_df_new[p_n_fs_w_df <= t] = 0
        G = nx.from_pandas_adjacency(p_n_fs_w_df_new, create_using=nx.Graph())
    # print(p_n_fs_w_df_new)
    print("The threshold value ", t)
    print("G is connected", nx.is_connected(G))
    return G


def get_node_embeddings(feature_df, G, ne_methods_dict):
    # G = get_Graph(feature_df, neighbor_num=neighbor_num)
    node_embeddings = [[] for node in range(len(feature_df))]
    from karateclub.node_embedding import Node2Vec, GraRep, SocioDim
    for ne_methods in ne_methods_dict.keys():
        if ne_methods not in ["Node2Vec", "GraRep", "LaplacianEigenmaps", "SocioDim"]:
            print("Error！The ne_methods_dicts may be set incorrectly.")

    if "Node2Vec" in ne_methods_dict.keys():
        print("Node2Vec")
        if isinstance(ne_methods_dict["Node2Vec"], list):
            for Node2Vec_parameter in ne_methods_dict["Node2Vec"]:
                node2vec = Node2Vec(
                    **Node2Vec_parameter)  # 参数有dimensions(128), epochs(1), workers(4), walk_number(10),walk_length(80),learning_rate(0.05),window_size(5)
                node2vec.fit(G)
                for i, vec in enumerate(node2vec.get_embedding()):
                    node_embeddings[i].extend(list(vec))
        elif isinstance(ne_methods_dict["Node2Vec"], dict):
            node2vec = Node2Vec(**ne_methods_dict["Node2Vec"])
            node2vec.fit(G)
            for i, vec in enumerate(node2vec.get_embedding()):
                node_embeddings[i].extend(list(vec))
        else:
            print("错误！")

    if "GraRep" in ne_methods_dict.keys():
        print("GraRep")
        if isinstance(ne_methods_dict["GraRep"], list):
            for GraRep_parameter in ne_methods_dict["GraRep"]:
                grarep = GraRep(**GraRep_parameter)  # 参数有dimensions(128), iteration(10), order(5)
                grarep.fit(G)
                for i, vec in enumerate(grarep.get_embedding()):
                    node_embeddings[i].extend(list(vec))
        elif isinstance(ne_methods_dict["GraRep"], dict):
            grarep = GraRep(
                **ne_methods_dict["GraRep"])
            grarep.fit(G)
            for i, vec in enumerate(grarep.get_embedding()):
                node_embeddings[i].extend(list(vec))
        else:
            print("错误！")

    if "SocioDim" in ne_methods_dict.keys():
        print("SocioDim")
        if isinstance(ne_methods_dict["SocioDim"], list):
            for SocioDim_parameter in ne_methods_dict["SocioDim"]:
                sociodim = SocioDim(
                    **SocioDim_parameter)  # 参数有dimensions(128)
                sociodim.fit(G)
                for i, vec in enumerate(sociodim.get_embedding()):
                    node_embeddings[i].extend(list(vec))
        elif isinstance(ne_methods_dict["SocioDim"], dict):
            sociodim = SocioDim(
                **ne_methods_dict["SocioDim"])
            sociodim.fit(G)
            for i, vec in enumerate(sociodim.get_embedding()):
                node_embeddings[i].extend(list(vec))
        else:
            print("Error！")

    print("finish graph embeddings training")

    node_embeddings_df = pd.DataFrame(node_embeddings)
    node_embeddings_df.index = feature_df.index

    if len(node_embeddings_df) == 0:
        print("Error！The ne_methods_dicts may be set incorrectly.")
    return node_embeddings_df
