from models.BaseModel import BaseModel
from catboost import CatBoostClassifier


class CatBoost_Model(BaseModel):

    def train(self, train_X, train_Y, validate_X=None, validate_Y=None, iterations=20000, learning_rate=0.0008,
              max_depth=6, early_stopping_rounds=2000, auto_class_weights=None, custom_loss=None, random_seed=42):
        if custom_loss is None:
            custom_loss = ['AUC']
        model = CatBoostClassifier(
            iterations=iterations,
            learning_rate=learning_rate,
            custom_loss=custom_loss,
            random_seed=random_seed,
            logging_level="Silent",
            max_depth=max_depth,
            eval_metric="AUC",
            task_type="CPU",
            early_stopping_rounds=early_stopping_rounds,
            auto_class_weights=auto_class_weights
        )
        if validate_X is None or validate_Y is None:
            model.fit(train_X,
                      train_Y)
        else:
            model.fit(train_X, train_Y, eval_set=(validate_X, validate_Y))
        self.model = model
        return model

    def predict(self, test_X):
        y_pred = self.model.predict(test_X)
        return y_pred

    def predict_score(self, test_X):
        y_score = self.model.predict_proba(test_X)[:, 1]
        return y_score
