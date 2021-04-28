# In this file, users can modify the parameters used in training model.
# Users can also add a new dataset, by adding a new item to the dataset_parameters_dict. The form of items are {"dataset"_ name":parameters}

dataset_parameters_dict = {"A101": {"features": ["PseKNC", "CTD", "NPS"],
                                    "neighbor_num": 20,
                                    "embeddings": {'GraRep': {'dimensions': 16, 'iteration': 40},
                                                   'Node2Vec': {'dimensions': 16},
                                                   'SocioDim': {'dimensions': 16}},
                                    "catboost": {}},
                           "A25": {"features": ["EIIP", "NCP-ND", "PseKNC", "NPPS-xi1", "NPPS-xi2", "NPS"],
                                   "neighbor_num": 5,
                                   "embeddings": {'GraRep': {'dimensions': 1, 'iteration': 10},
                                                  'Node2Vec': {'dimensions': 8},
                                                  'SocioDim': {'dimensions': 4}},
                                   "catboost": {}},
                           "S21": {"features": ["NCP-ND", "NPPS-xi1", "NPPS-xi2"],
                                   "neighbor_num": 1500,
                                   "embeddings": {'GraRep': {'dimensions': 4, 'iteration': 50},
                                                  'Node2Vec': {'dimensions': 16},
                                                  'SocioDim': {'dimensions': 8}},
                                   "catboost": {"auto_class_weights": "Balanced"}},
                           "H41": {"features": ["NCP-ND", "PseKNC", "NPPS-xi1"],
                                   "neighbor_num": 620,
                                   "embeddings": {'GraRep': {'dimensions': 8, 'iteration': 40},
                                                  'Node2Vec': {'dimensions': 8},
                                                  'SocioDim': {'dimensions': 4}},
                                   "catboost": {}}
                           }
