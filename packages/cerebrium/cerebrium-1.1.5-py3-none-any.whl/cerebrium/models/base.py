from abc import ABC, abstractmethod
from enum import Enum
from typing import Union, List

from numpy import ndarray

from torch import Tensor


# from sklearn.base import BaseEstimator
# from torch.nn import Module as TorchModule
# from transformers import Pipeline
# from spacy.language import Language
# from onnxruntime import InferenceSession


class ModelType(Enum):
    XGBOOST_CLASSIFIER = "xgboost_classifier"
    XGBOOST_REGRESSOR = "xgboost_regressor"
    TORCH = "torch"
    SKLEARN = "sklearn"
    SKLEARN_CLASSIFIER = "sklearn_classifier"
    ONNX = "onnx"
    SKLEARN_PREPROCESSOR = "sklearn_preprocessor"
    PREBUILT = "prebuilt"
    SPACY = "spacy"
    HUGGINGFACE_PIPELINE = "hf_pipeline"


class BaseModel(ABC):
    def __init__(
        self,
        model,
    ):
        self.model = model

    @abstractmethod
    def predict(self, input: Union[Tensor, ndarray, List]) -> list:
        pass
