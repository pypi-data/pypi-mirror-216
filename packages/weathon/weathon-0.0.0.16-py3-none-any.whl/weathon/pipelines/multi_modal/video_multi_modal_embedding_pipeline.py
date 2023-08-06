from typing import Any, Dict

from weathon.utils.constants.metainfo import Pipelines
from weathon.pipelines.base import Input, Pipeline
from weathon.registry import PIPELINES
from weathon.utils.constants import Tasks
from weathon.utils.device import device_placement
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.video_multi_modal_embedding,
    module_name=Pipelines.video_multi_modal_embedding)
class VideoMultiModalEmbeddingPipeline(Pipeline):

    def __init__(self, model: str, **kwargs):
        """
        use `model` to create a video_multi_modal_embedding pipeline for prediction
        Args:
            model: model id on modelscope hub.
        """
        super().__init__(model=model)

    def preprocess(self, input: Input) -> Dict[str, Any]:
        return input

    def _process_single(self, input: Input, *args, **kwargs) -> Dict[str, Any]:
        with device_placement(self.framework, self.device_name):
            out = self.forward(input)

        self._check_output(out)
        return out

    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:
        return self.model(input)

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return inputs
