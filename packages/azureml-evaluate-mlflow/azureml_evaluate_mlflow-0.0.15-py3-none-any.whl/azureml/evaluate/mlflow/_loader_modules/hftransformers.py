# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os

from mlflow import MlflowException

import azureml.evaluate.mlflow as mlflow
from mlflow.utils.model_utils import _get_flavor_configuration

_logger = logging.getLogger(__name__)


class _AzureMLTransformersWrapper(mlflow.hftransformers._HFTransformersWrapper):
    def predict(self, data, **kwargs):
        if hasattr(self.hf_model, 'eval'):
            self.hf_model.eval()
        data, addn_args = self._validate_data(data)
        from azureml.evaluate.mlflow.hftransformers._task_based_predictors import get_predictor
        predictor_kwargs = {**self.misc_conf, **kwargs, **addn_args}
        self.task_type = predictor_kwargs.pop("task_type", self.task_type)
        problem_type = self._get_problem_type(**predictor_kwargs)
        if hasattr(self.config, 'custom_pipelines'):
            setattr(self.config, 'custom_pipelines', self.custom_pipelines)
        predictor = get_predictor(self.task_type, problem_type)(task_type=self.task_type, model=self.hf_model,
                                                                tokenizer=self.tokenizer,
                                                                config=self.config)
        return predictor.predict(data, **predictor_kwargs)

    def predict_proba(self, data, **kwargs):
        if hasattr(self.hf_model, 'eval'):
            self.hf_model.eval()
        data, addn_args = self._validate_data(data)
        from azureml.evaluate.mlflow.hftransformers._task_based_predictors import get_predictor
        predictor_kwargs = {**self.misc_conf, **kwargs, **addn_args}
        self.task_type = predictor_kwargs.pop("task_type", self.task_type)
        problem_type = self._get_problem_type(**predictor_kwargs)
        if hasattr(self.config, 'custom_pipelines'):
            setattr(self.config, 'custom_pipelines', self.custom_pipelines)
        predictor = get_predictor(self.task_type, problem_type)(task_type=self.task_type, model=self.hf_model,
                                                                tokenizer=self.tokenizer,
                                                                config=self.config)
        return predictor.predict_proba(data, **predictor_kwargs)


def _load_azureml(path, **kwargs):
    """
    Load PyFunc implementation. Called by ``pyfunc.load_model``.

    :param path: Local filesystem path to the MLflow Model with the ``pytorch`` flavor.
    """
    path1 = os.sep.join(path.split(os.sep)[:-1])
    try:
        hf_conf = _get_flavor_configuration(path1, mlflow.hftransformers.FLAVOR_NAME_MLMODEL_LOGGING)
    except MlflowException as e:
        hf_conf = _get_flavor_configuration(path1, mlflow.hftransformers.FLAVOR_NAME)
    task_type, hf_model, tokenizer, config = mlflow.hftransformers._load_model(path, hf_conf)
    hf_conf["path"] = path1
    return _AzureMLTransformersWrapper(task_type, hf_model, tokenizer, config, hf_conf)
