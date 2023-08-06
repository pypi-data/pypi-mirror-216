from sklearn.base import BaseEstimator,TransformerMixin
class CustomEncoder_(BaseEstimator, TransformerMixin):
    def __init__(self, col):
        self.col = col
        self.enc_map = {}
        
    def fit(self, X, y=None):
        unique_values = sorted(list(X[self.col].drop_duplicates()))
        self.enc_map = {unique_values[i]: i for i in range(len(unique_values))}
        return self
    
    def transform(self, X):
        X_encoded = X.copy()
        X_encoded[self.col] = X_encoded[self.col].replace(list(self.enc_map.keys()),list(self.enc_map.values()))
        return X_encoded