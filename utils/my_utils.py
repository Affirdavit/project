# Custom class for day of week and month of year, using Cyclical Encoding due to its circular nature
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

main_color = '#69b3a2'


class CyclicalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns, max_vals):
        self.columns = columns
        self.max_vals = max_vals
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        for col, max_val in zip(self.columns, self.max_vals):
            X[col + '_sin'] = np.sin(2 * np.pi * X[col] / max_val)
            X[col + '_cos'] = np.cos(2 * np.pi * X[col] / max_val)
            X.drop(columns=[col], inplace=True)
        return X
    
