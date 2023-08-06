"""A Pipeline for calibrated modeling."""
from __future__ import annotations

import logging
import os
import pickle
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import torch
from pydantic import BaseModel, Field

from .data import CSVData, determine_feature_types, replace_missing_values
from .enums import FeatureType, LossType, Metric, TargetType
from .models import CalibratedLinear
from .training import train_and_evaluate_model
from .types import (
    CategoricalFeatureConfig,
    Dataset,
    DatasetSplit,
    LinearConfig,
    NumericalFeatureConfig,
    PipelineConfig,
    PreparedData,
    TrainingConfig,
    TrainingResults,
)


class Pipeline:  # pylint: disable=too-many-instance-attributes
    """A pipeline for calibrated modeling.

    The pipeline defines the configuration for training a calibrated model. The
    pipeline itself defines the features, target, and target type to be used. When
    training a model, the data and configuration used will be versioned and stored in
    the pipeline. The pipeline can be used to train multiple models with different
    configurations if desired; however, the target, target type, and primary metric
    should not be changed after initialization so that models trained by this pipeline
    can be compared.

    Example:

    ```python
    data = pd.read_csv(...)
    pipeline = Pipeline(features, target, TargetType.CLASSIFICATION)
    trained_model = pipeline.train(data)
    ```

    Attributes:
        ...
    """

    def __init__(
        self,
        features: List[str],
        target: str,
        target_type: TargetType,
        categories: Optional[Dict[str, List[str]]] = None,
        primary_metric: Optional[Metric] = None,
        name: Optional[str] = None,
    ):
        """Initializes an instance of `Pipeline`.

        The pipeline is initialized with a default config, which can be modified later.
        The target type can be optionally specfified. The default primary metric will be
        AUC for classification and Mean Squared Error for regression if not specified.

        Args:
            features: The column names in your data to use as features.
            target: The name of the target column.
            target_type: The type of the target column.
            categories: A dictionary mapping feature names to unique categories. Any
                values not in the categories list for a given feature will be treated
                as a missing value.
            primary_metric: The primary metric to use for training and evaluation.
            name: The name of the pipeline. If not provided, the name will be set to
                `{target}_{target_type}`.
        """
        self.name: str = name if name else f"{target}_{target_type}"
        self.target: str = target
        self.target_type: TargetType = target_type
        self.primary_metric: Metric = (
            primary_metric
            if primary_metric is not None
            else (
                Metric.AUC
                if self.target_type == TargetType.CLASSIFICATION
                else Metric.MSE
            )
        )
        self.feature_configs: Dict[
            str, Union[CategoricalFeatureConfig, NumericalFeatureConfig]
        ] = {
            feature_name: (
                CategoricalFeatureConfig(
                    name=feature_name,
                    categories=categories[feature_name],
                )
                if categories and feature_name in categories
                else NumericalFeatureConfig(name=feature_name)
            )
            for feature_name in features
        }
        self.shuffle_data: bool = True
        self.drop_empty_percentage: int = 70
        self.dataset_split: DatasetSplit = DatasetSplit(train=80, val=10, test=10)

        # Maps a pipeline config id to its corresponding `PipelineConfig`` instance.
        self.configs: Dict[int, PipelineConfig] = {}
        # Maps a dataset id to its corresponding `Dataset`` instance.
        self.datasets: Dict[int, Dataset] = {}

    def prepare(  # pylint: disable=too-many-locals
        self,
        data: pd.DataFrame,
        pipeline_config_id: Optional[int] = None,
    ) -> Tuple[Dataset, PipelineConfig]:
        """Prepares the data and versions it along with the current pipeline config.

        If any features in data are detected as non-numeric, the pipeline will attempt
        to handle them as categorical features. Any features that the pipeline cannot
        handle will be skipped.

        Args:
            data: The raw data to be prepared for training.
            pipeline_config_id: The id of the pipeline config to be used for training.
                If not provided, the current pipeline config will be used and versioned.

        Returns:
            A tuple of the versioned dataset and pipeline config.
        """
        data.replace("", np.nan, inplace=True)  # treat empty strings as NaN
        if pipeline_config_id is None:
            pipeline_config_id = len(self.configs)
            pipeline_config = self._version_pipeline_config(data, pipeline_config_id)
            self.configs[pipeline_config_id] = pipeline_config
        else:
            pipeline_config = self.configs[pipeline_config_id]

        # Select only the features defined in the pipeline config.
        data = data[list(pipeline_config.feature_configs.keys()) + [self.target]]
        # Drop rows with too many missing values according to the drop empty percent.
        max_num_empty_columns = int(
            (pipeline_config.drop_empty_percentage * data.shape[1]) / 100
        )
        data = data[data.isnull().sum(axis=1) <= max_num_empty_columns]
        # Replace any missing values (i.e. NaN) with missing value constants.
        data = replace_missing_values(data, pipeline_config.feature_configs)
        if pipeline_config.shuffle_data:
            data = data.sample(frac=1).reset_index(drop=True)
        train_percentage = pipeline_config.dataset_split.train / 100
        train_data = data.iloc[: int(len(data) * train_percentage)]
        val_percentage = pipeline_config.dataset_split.val / 100
        val_data = data.iloc[
            int(len(data) * train_percentage) : int(
                len(data) * (train_percentage + val_percentage)
            )
        ]
        test_data = data.iloc[int(len(data) * (train_percentage + val_percentage)) :]

        dataset_id = len(self.datasets)
        dataset = Dataset(
            id=dataset_id,
            pipeline_config_id=pipeline_config_id,
            prepared_data=PreparedData(train=train_data, val=val_data, test=test_data),
        )
        self.datasets[dataset_id] = dataset

        return dataset, pipeline_config

    def train(
        self,
        data: Union[pd.DataFrame, int],
        pipeline_config_id: Optional[int] = None,
        model_config: Optional[LinearConfig] = None,
        training_config: Optional[TrainingConfig] = None,
    ) -> TrainedModel:
        """Returns a calibrated model trained according to the given configs.

        Args:
            data: The raw data to be prepared and trained on. If an int is provided,
                it is assumed to be a dataset id and the corresponding dataset will be
                used.
            pipeline_config_id: The id of the pipeline config to be used for training.
                If not provided, the current pipeline config will be versioned and used.
                If data is an int, this argument is ignored and the pipeline config used
                to prepare the data with the given id will be used.
            model_config: The config to be used for training the model. If not provided,
                a default config will be used.
            training_config: The config to be used for training the model. If not
                provided, a default config will be used.

        Returns:
            A `TrainedModel` instance.
        """
        if isinstance(data, int):
            dataset = self.datasets[data]
            pipeline_config = self.configs[dataset.pipeline_config_id]
        else:
            dataset, pipeline_config = self.prepare(data, pipeline_config_id)

        if model_config is None:
            model_config = LinearConfig()

        if training_config is None:
            training_config = TrainingConfig(
                loss_type=LossType.BINARY_CROSSENTROPY
                if self.target_type == TargetType.CLASSIFICATION
                else LossType.MSE
            )

        model, training_results = train_and_evaluate_model(
            dataset,
            self.target,
            self.primary_metric,
            pipeline_config,
            model_config,
            training_config,
        )

        return TrainedModel(
            dataset_id=dataset.id,
            pipeline_config=pipeline_config,
            model_config=model_config,
            training_config=training_config,
            training_results=training_results,
            model=model,
        )

    def save(self, filepath: str):
        """Saves the pipeline to the specified filepath.

        Args:
            filepath: The directory to which the pipeline wil be saved. If the directory
                does not exist, this function will attempt to create it. If the
                directory already exists, this function will overwrite any existing
                content with conflicting filenames.
        """
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(os.path.join(filepath, "pipeline.pkl"), "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filepath: str) -> Pipeline:
        """Loads the pipeline from the specified filepath.

        Args:
            filepath: The filepath from which to load the pipeline. The filepath should
                point to a file created by the `save` method of a `TrainedModel`
                instance.

        Returns:
            A `Pipeline` instance.
        """
        with open(os.path.join(filepath, "pipeline.pkl"), "rb") as file:
            pipeline = pickle.load(file)

        return pipeline

    ############################################################################
    #                            Private Methods                               #
    ############################################################################

    def _version_pipeline_config(self, data: pd.DataFrame, pipeline_config_id: int):
        """Returns a new `PipelineConfig` instance verisoned from the current config."""
        pipeline_config = PipelineConfig(
            id=pipeline_config_id,
            target=self.target,
            target_type=self.target_type,
            primary_metric=self.primary_metric,
            feature_configs=self.feature_configs,
            shuffle_data=self.shuffle_data,
            drop_empty_percentage=self.drop_empty_percentage,
            dataset_split=self.dataset_split,
        )

        feature_types = determine_feature_types(
            data[list(pipeline_config.feature_configs.keys())]
        )
        for feature_name, feature_type in feature_types.items():
            feature_config = pipeline_config.feature_configs[feature_name]
            if (
                feature_type == FeatureType.NUMERICAL
                or feature_config.type == FeatureType.CATEGORICAL
            ):
                continue
            if feature_type == FeatureType.CATEGORICAL:
                logging.info(
                    "Detected %s as categorical. Replacing numerical config with "
                    "default categorical config using unique values as categories",
                    feature_name,
                )
                pipeline_config.feature_configs[
                    feature_name
                ] = CategoricalFeatureConfig(
                    name=feature_name,
                    categories=sorted(data[feature_name].dropna().unique().tolist()),
                )
            else:
                logging.info(
                    "Removing feature %s because its data type is not supported.",
                    feature_name,
                )
                pipeline_config.feature_configs.pop(feature_name)

        return pipeline_config


class TrainedModel(BaseModel):
    """A trained calibrated model.

    This model is a container for a trained calibrated model that provides useful
    methods for using the model. The trained calibrated model is the result of running
    the `train` method of a `Pipeline` instance.

    Example:

    ```python
    data = pd.read_csv("data.csv")
    predictions = trained_model.predict(data)
    trained_model.analyze()
    ```
    """

    dataset_id: int = Field(...)
    pipeline_config: PipelineConfig = Field(...)
    model_config: LinearConfig = Field(...)
    training_config: TrainingConfig = Field(...)
    training_results: TrainingResults = Field(...)
    model: CalibratedLinear = Field(...)

    class Config:  # pylint: disable=missing-class-docstring,too-few-public-methods
        arbitrary_types_allowed = True

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Returns predictions for the given data.

        Args:
            data: The data to be used for prediction. Must have all columns used for
                training the model to be used.

        Returns:
            If the target type is regression, a numpy array of predictions. If the
            target type is classification, a tuple containing a numpy array of
            predictions (logits) and a numpy array of probabilities.
        """
        data = data.loc[:, list(self.pipeline_config.feature_configs.keys())]
        data = replace_missing_values(data, self.pipeline_config.feature_configs)

        csv_data = CSVData(data)
        csv_data.prepare(self.model.features, None)
        inputs = list(csv_data.batch(csv_data.num_examples))[0]
        with torch.no_grad():
            predictions = self.model(inputs).numpy()

        if self.pipeline_config.target_type == TargetType.REGRESSION:
            return predictions

        return predictions, 1.0 / (1.0 + np.exp(-predictions))

    def analysis(self):
        """Charts the results for the specified trained model in the SOTAI web client.

        This function requires an internet connection and a SOTAI account. The trained
        model will be uploaded to the SOTAI web client for analysis.

        If you would like to analyze the results for a trained model without uploading
        it to the SOTAI web client, the data is available in `training_results`.
        """
        raise NotImplementedError()

    def save(self, filepath: str):
        """Saves the trained model to the specified directory.

        Args:
            filepath: The directory to save the trained model to. If the directory does
                not exist, this function will attempt to create it. If the directory
                already exists, this function will overwrite any existing content with
                conflicting filenames.
        """
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(os.path.join(filepath, "trained_model_metadata.pkl"), "wb") as file:
            pickle.dump(self.dict(exclude={"model"}), file)
        model_path = f"{filepath}/trained_ptcm_model.pt"
        torch.save(self.model, model_path)

    @classmethod
    def load(cls, filepath: str) -> TrainedModel:
        """Loads a trained model from the specified filepath.

        Args:
            filepath: The filepath to load the trained model from. The filepath should
                point to a file created by the `save` method of a `TrainedModel`
                instance.

        Returns:
            A `TrainedModel` instance.
        """
        with open(os.path.join(filepath, "trained_model_metadata.pkl"), "rb") as file:
            trained_model_metadata = pickle.load(file)
        model_path = f"{filepath}/trained_ptcm_model.pt"
        model = torch.load(model_path)
        model.eval()

        return TrainedModel(**trained_model_metadata, model=model)
