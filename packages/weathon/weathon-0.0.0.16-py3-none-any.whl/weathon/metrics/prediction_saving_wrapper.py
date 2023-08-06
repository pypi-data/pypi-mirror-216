from typing import Dict

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

from weathon.base import BaseMetric
from weathon.registry import METRICS
from weathon.registry.registry import default_group
from weathon.utils.constants.metainfo import Metrics


@METRICS.register_module(group_key=default_group, module_name=Metrics.prediction_saving_wrapper)
class PredictionSavingWrapper(BaseMetric):
    """The wrapper to save predictions to file.
    Args:
        saving_fn: The saving_fn used to save predictions to files.
    """

    def __init__(self, saving_fn, **kwargs):
        super().__init__(**kwargs)
        self.saving_fn = saving_fn

    def add(self, outputs: Dict, inputs: Dict):
        self.saving_fn(inputs, outputs)

    def evaluate(self):
        return {}

    def merge(self, other: 'PredictionSavingWrapper'):
        pass

    def __getstate__(self):
        pass

    def __setstate__(self, state):
        pass
