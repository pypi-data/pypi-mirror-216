from typing import Any, Dict

from weathon.utils.constants.metainfo import Pipelines
from weathon.outputs import OutputKeys
from weathon.pipelines.base import Input, Model, Pipeline
from weathon.registry import PIPELINES
from weathon.utils.constants import Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.video_depth_estimation, module_name=Pipelines.video_depth_estimation)
class VideoDepthEstimationPipeline(Pipeline):

    def __init__(self, model: str, **kwargs):
        """
        use `model` to create a video depth estimation pipeline for prediction
        Args:
            model: model id on modelscope hub.
        """
        super().__init__(model=model, **kwargs)

        logger.info('depth estimation model, pipeline init')

    def preprocess(self, input: Input) -> Dict[str, Any]:
        video_path = input
        data = {'video_path': video_path}

        return data

    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:
        results = self.model.inference(input)
        return results

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        results = self.model.postprocess(inputs)
        depths = results['depths']
        depths_color = results['depths_color']
        poses = results['poses']

        outputs = {
            OutputKeys.DEPTHS: depths,
            OutputKeys.DEPTHS_COLOR: depths_color,
            OutputKeys.POSES: poses
        }

        return outputs
