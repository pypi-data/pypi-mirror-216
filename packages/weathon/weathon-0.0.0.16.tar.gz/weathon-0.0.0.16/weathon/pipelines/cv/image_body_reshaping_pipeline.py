from typing import Any, Dict

from weathon.utils.constants.metainfo import Pipelines
from weathon.outputs import OutputKeys
from weathon.pipelines.base import Input, Pipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import LoadImage
from weathon.utils.constants import ModelFile, Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.image_body_reshaping, module_name=Pipelines.image_body_reshaping)
class ImageBodyReshapingPipeline(Pipeline):

    def __init__(self, model: str, **kwargs):
        """
        use `model` to create a image body reshaping pipeline for prediction
        Args:
            model: model id on modelscope hub.
        """
        super().__init__(model=model, **kwargs)
        logger.info('body reshaping model init done')

    def preprocess(self, input: Input) -> Dict[str, Any]:
        img = LoadImage.convert_to_ndarray(input)
        result = {'img': img}
        return result

    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:
        output = self.model.inference(input['img'])
        result = {'outputs': output}
        return result

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        output_img = inputs['outputs']
        return {OutputKeys.OUTPUT_IMG: output_img}
