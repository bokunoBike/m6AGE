class BaseModel:
    def __init__(self):
        self.model = None

    def train(self, train_X, train_Y):  # Deferred to the subclass implementation
        return self.model

    def predict(self, test_X):  # Deferred to the subclass implementation
        if self.model is None:
            print("Error! Model is None!")
        y_pred = []
        # y_pred = self.grid_model.predict(test_X)
        return y_pred

    def predict_score(self, test_X):  # Deferred to the subclass implementation
        if self.model is None:
            print("Error! Model is None!")
        y_score = []
        return y_score

    def train_predict_pred_score(self, train_X, train_Y, test_X, model_func_args=None):
        if model_func_args is None:
            model_func_args = {}
        self.train(train_X=train_X, train_Y=train_Y, **model_func_args)
        y_pred = self.predict(test_X)
        y_score = self.predict_score(test_X)
        return y_pred, y_score

    def cross_train_predict(self, X, Y, fold=5, model_func_args=None, random_state=12):
        return

    def predict_with_threshold(self, test_X, threshold):
        y_score = self.predict_score(test_X=test_X)
        y_pred = []
        for score in y_score:
            if score > threshold:
                y_pred.append(1)
            else:
                y_pred.append(0)
        return y_pred