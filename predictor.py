import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor

import numpy as np

class Predictor:
    """数据预测类"""
    def __init__(self, is_linear):
        self.predictor = LinearRegression() \
            if is_linear else KNeighborsRegressor()
        self.start_index = None

    def fit(self, col_df: pd.DataFrame) -> float:  # 返回模型的拟合程度
        x = col_df.index.values
        self.start_index = len(x)
        x = np.reshape(x, (-1, 1))
        y = col_df.values
        self.predictor.fit(x, y)
        return self.predictor.score(x, y)

    def predict(self, n_predicts: int):
        # 给一列数据，并向后预测n_predicts个新数据
        if self.start_index is None: raise Exception('Predictor not be fitted!')
        x_test = np.reshape(np.arange(self.start_index, self.start_index + n_predicts), (-1, 1))
        preds = self.predictor.predict(x_test)
        return preds
