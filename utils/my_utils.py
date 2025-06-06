# Custom class for day of week and month of year, using Cyclical Encoding due to its circular nature
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

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
    
def reduce_mem_usage(df, verbose=True):
    start_mem = df.memory_usage(deep=True).sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes

        if col_type == 'object' or col_type.name == 'category':
            continue  # skip strings/categories

        c_min = df[col].min()
        c_max = df[col].max()

        if str(col_type)[:3] == 'int':
            if c_min >= 0:
                if c_max < 255:
                    df[col] = df[col].astype(np.uint8)
                elif c_max < 65535:
                    df[col] = df[col].astype(np.uint16)
                elif c_max < 4294967295:
                    df[col] = df[col].astype(np.uint32)
                else:
                    df[col] = df[col].astype(np.uint64)
            else:
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                else:
                    df[col] = df[col].astype(np.int64)

        elif str(col_type)[:5] == 'float':
            if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                df[col] = df[col].astype(np.float16)
            elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                df[col] = df[col].astype(np.float32)
            else:
                df[col] = df[col].astype(np.float64)

    end_mem = df.memory_usage(deep=True).sum() / 1024**2
    if verbose:
        print(f'Memory usage reduced from {start_mem:.2f} MB to {end_mem:.2f} MB '
              f'({100 * (start_mem - end_mem) / start_mem:.1f}% reduction)')

    return df

def create_time_weights(n_samples, decay_factor=0.95):
    """
    Create exponentially decaying weights based on sample position.
    More recent samples (higher indices) get higher weights.
    decay_factor controls the rate of decay (0.95 = 5% decay per time unit)
    """
    positions = np.arange(n_samples)
    # Normalize positions to [0, 1] range
    normalized_positions = positions / (n_samples - 1)
    # Apply exponential weighting
    weights = decay_factor ** (1 - normalized_positions)
    # Normalize weights to sum to n_samples (maintains scale)
    weights = weights * n_samples / weights.sum()
    return weights