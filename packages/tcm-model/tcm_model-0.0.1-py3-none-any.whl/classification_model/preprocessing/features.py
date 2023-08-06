import re

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from classification_model.config.core import config


class ExtractLetterTransformer(BaseEstimator, TransformerMixin):
    # Extract fist letter of variable

    def __init__(self, variables):
        if not isinstance(variables, list):
            raise ValueError("variables should be a list")
        self.variables = variables

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        X = X.copy()
        for feature in self.variables:
            X[feature] = X[feature].str[0]

        return X


class PreprocessData(BaseEstimator, TransformerMixin):
    # Extract fist letter of variable

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        X = X.copy()

        def get_first_cabin(row) -> str:
            try:
                return row.split()[0]
            except Exception:
                return np.nan

        def get_title(passenger) -> str:
            line = passenger
            if re.search("Mrs", line):
                return "Mrs"
            elif re.search("Mr", line):
                return "Mr"
            elif re.search("Miss", line):
                return "Miss"
            elif re.search("Master", line):
                return "Master"
            else:
                return "Other"

        X = X.replace("?", np.nan)

        X["cabin"] = X["cabin"].apply(get_first_cabin)

        X["title"] = X["name"].apply(get_title)

        X["fare"] = X["fare"].astype("float")
        X["age"] = X["age"].astype("float")

        X.drop(labels=config.model_config.drop_features, axis=1, inplace=True)

        return X
