from pipeline import titanic_pipeline
from sklearn.model_selection import train_test_split

from classification_model.config.core import config
from classification_model.preprocessing.data_manager import load_dataset, save_pipeline


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.raw_data)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )

    # fit model
    titanic_pipeline.fit(X_train, y_train)

    # persist trained model
    save_pipeline(pipeline_to_persist=titanic_pipeline)


if __name__ == "__main__":
    run_training()
