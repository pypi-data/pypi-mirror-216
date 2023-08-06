from typing import Any, Dict, Optional

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.multi_modal import (
    MultiStageDiffusionForTextToImageSynthesis, OfaForTextToImageSynthesis)
from weathon.outputs import OutputKeys
from weathon.pipelines.base import Input, Pipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import OfaPreprocessor, Preprocessor
from weathon.utils.constants import Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.text_to_image_synthesis,
    module_name=Pipelines.text_to_image_synthesis)
class TextToImageSynthesisPipeline(Pipeline):

    def __init__(self,
                 model: str,
                 preprocessor: Optional[Preprocessor] = None,
                 **kwargs):
        """
        use `model` and `preprocessor` to create a kws pipeline for prediction
        Args:
            model: model id on modelscope hub.
        """
        super().__init__(model=model, preprocessor=preprocessor, **kwargs)
        if preprocessor is None and isinstance(self.model,
                                               OfaForTextToImageSynthesis):
            self.preprocessor = OfaPreprocessor(self.model.model_dir)

    def preprocess(self, input: Input, **preprocess_params) -> Dict[str, Any]:
        if self.preprocessor is not None:
            return self.preprocessor(input, **preprocess_params)
        else:
            return input

    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(self.model,
                      (OfaForTextToImageSynthesis,
                       MultiStageDiffusionForTextToImageSynthesis)):
            return self.model(input)
        return self.model.generate(input)

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(inputs, list):
            inputs = [inputs]
        return {OutputKeys.OUTPUT_IMGS: inputs}
