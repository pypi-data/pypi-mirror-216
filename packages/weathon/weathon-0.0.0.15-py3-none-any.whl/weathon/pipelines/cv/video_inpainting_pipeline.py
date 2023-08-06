# Copyright 2021-2022 The Alibaba Fundamental Vision Team Authors. All rights reserved.
from typing import Any, Dict

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.cv.video_inpainting import inpainting
from weathon.outputs import OutputKeys
from weathon.pipelines.base import Input, Pipeline
from weathon.registry import PIPELINES
from weathon.utils.constants import Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.video_inpainting, module_name=Pipelines.video_inpainting)
class VideoInpaintingPipeline(Pipeline):

    def __init__(self, model: str, **kwargs):
        """
        use `model` to create video inpainting pipeline for prediction
        Args:
            model: model id on modelscope hub.
        """

        super().__init__(model=model, **kwargs)
        logger.info('load model done')

    def preprocess(self, input: Input) -> Dict[str, Any]:
        return input

    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:
        decode_error, fps, w, h = inpainting.video_process(
            input['video_input_path'])

        if decode_error is not None:
            return {OutputKeys.OUTPUT: 'decode_error'}

        inpainting.inpainting_by_model_balance(self.model,
                                               input['video_input_path'],
                                               input['mask_path'],
                                               input['video_output_path'], fps,
                                               w, h)

        return {OutputKeys.OUTPUT: 'Done'}

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return inputs
