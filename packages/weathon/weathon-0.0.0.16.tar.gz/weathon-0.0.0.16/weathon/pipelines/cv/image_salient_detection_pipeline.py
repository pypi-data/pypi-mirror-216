from typing import Any, Dict

from weathon.utils.constants.metainfo import Pipelines
from weathon.outputs import OutputKeys
from weathon.pipelines.base import Input, Pipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import LoadImage
from weathon.utils.constants import Tasks


@PIPELINES.register_module(
    Tasks.semantic_segmentation, module_name=Pipelines.salient_detection)
@PIPELINES.register_module(
    Tasks.semantic_segmentation,
    module_name=Pipelines.salient_boudary_detection)
@PIPELINES.register_module(
    Tasks.semantic_segmentation, module_name=Pipelines.camouflaged_detection)
class ImageSalientDetectionPipeline(Pipeline):

    def __init__(self, model: str, **kwargs):
        """
            model: model id on modelscope hub.
        """
        super().__init__(model=model, auto_collate=False, **kwargs)

    def preprocess(self, input: Input) -> Dict[str, Any]:

        img = LoadImage.convert_to_ndarray(input)
        img_h, img_w, _ = img.shape
        img = self.model.preprocess(img)
        result = {'img': img, 'img_w': img_w, 'img_h': img_h}
        return result

    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:

        outputs = self.model.inference(input['img'])
        result = {
            'data': outputs,
            'img_w': input['img_w'],
            'img_h': input['img_h']
        }
        return result

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:

        data = self.model.postprocess(inputs)
        outputs = {OutputKeys.MASKS: data}
        return outputs
