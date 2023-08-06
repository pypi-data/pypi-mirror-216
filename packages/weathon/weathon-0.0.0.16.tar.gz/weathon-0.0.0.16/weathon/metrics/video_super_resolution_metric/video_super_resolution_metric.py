from typing import Dict

import numpy as np
from datasets import Metric

from weathon.registry import METRICS
from weathon.registry.registry import default_group
from weathon.utils.constants.metainfo import Metrics
from weathon.metrics.video_super_resolution_metric.niqe import calculate_niqe
from weathon.utils.constants.metric_constant import MetricKeys


@METRICS.register_module(group_key=default_group, module_name=Metrics.video_super_resolution_metric)
class VideoSuperResolutionMetric(Metric):
    """The metric computation class for real-world video super-resolution classes.
    """
    pred_name = 'pred'

    def __init__(self):
        super(VideoSuperResolutionMetric, self).__init__()
        self.preds = []

    def add(self, outputs: Dict, inputs: Dict):
        eval_results = outputs[VideoSuperResolutionMetric.pred_name]
        self.preds.append(eval_results)

    def evaluate(self):
        niqe_list = []
        for pred in self.preds:
            if isinstance(pred, list):
                for item in pred:
                    niqe_list.append(
                        calculate_niqe(
                            item[0].permute(1, 2, 0).numpy() * 255,
                            crop_border=0))
            else:
                niqe_list.append(
                    calculate_niqe(
                        pred[0].permute(1, 2, 0).numpy() * 255, crop_border=0))
        return {MetricKeys.NIQE: np.mean(niqe_list)}

    def merge(self, other: 'VideoSuperResolutionMetric'):
        self.preds.extend(other.preds)

    def __getstate__(self):
        return self.preds

    def __setstate__(self, state):
        self.__init__()
        self.preds = state
