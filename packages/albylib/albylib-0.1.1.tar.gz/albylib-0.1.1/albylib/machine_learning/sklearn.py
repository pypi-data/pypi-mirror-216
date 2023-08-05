from sklearn.base import BaseEstimator, TransformerMixin


class FeatureSelector(BaseEstimator, TransformerMixin):
    """Selects columns. Useful for feature engineering"""

    def __init__(self, columns):
        """Save columns."""
        self.columns = columns

    def fit(self, X, y=None):
        """Do nothing."""
        return self

    def transform(self, X, y=None):
        """Select the columns."""
        return X[self.columns]
