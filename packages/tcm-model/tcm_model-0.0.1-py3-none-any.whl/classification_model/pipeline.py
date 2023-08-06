from feature_engine.encoding import OrdinalEncoder, RareLabelEncoder
from feature_engine.imputation import (
    AddMissingIndicator,
    CategoricalImputer,
    MeanMedianImputer,
)
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import classification_model.preprocessing.features as pp
from classification_model.config.core import config

titanic_pipeline = Pipeline(
    [
        ("preprocessor", pp.PreprocessData()),
        (
            "Letter_extractor",
            pp.ExtractLetterTransformer(variables=config.model_config.cabin_vars),
        ),
        (
            "missing_imputer",
            CategoricalImputer(
                imputation_method="missing", variables=config.model_config.cabin_vars
            ),
        ),
        (
            "freq_imputer",
            CategoricalImputer(
                imputation_method="frequent", variables=config.model_config.freq_impute
            ),
        ),
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_config.num_with_na),
        ),
        (
            "mean_imputer",
            MeanMedianImputer(
                imputation_method="mean", variables=config.model_config.num_with_na
            ),
        ),
        (
            "rare_encoder",
            RareLabelEncoder(
                tol=0.01, n_categories=1, variables=config.model_config.cat_vars
            ),
        ),
        (
            "cat_encoder",
            OrdinalEncoder(
                encoding_method="ordered", variables=config.model_config.cat_vars
            ),
        ),
        ("scaler", StandardScaler()),
        ("log_reg", LogisticRegression(random_state=config.model_config.random_state)),
    ]
)
