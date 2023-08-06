# Copyright 2021-2022 The Alibaba Fundamental Vision Team Authors. All rights reserved.

from typing import Any, Dict

import numpy as np

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.cv.product_segmentation import seg_infer
from weathon.outputs import OutputKeys
from weathon.pipelines.base import Input, Pipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import LoadImage
from weathon.utils.constants import Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.product_segmentation, module_name=Pipelines.product_segmentation)
class F3NetForProductSegmentationPipeline(Pipeline):

    def __init__(self, model: str, **kwargs):
        """
        use `model` to create product segmentation pipeline for prediction
        Args:
            model: model id on modelscope hub.
        """

        super().__init__(model=model, **kwargs)
        logger.info('load model done')

    def preprocess(self, input: Input) -> Dict[str, Any]:
        img = LoadImage.convert_to_ndarray(input['input_path'])
        img = img.astype(np.float32)
        return img

    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:

        mask = seg_infer.inference(self.model, self.device, input)
        return {OutputKeys.MASKS: mask}

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return inputs
