from typing import Any, Dict

from weathon.utils.constants.metainfo import Pipelines
from weathon.outputs import OutputKeys
from weathon.pipelines.base import Input, Pipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import LoadImage
from weathon.utils.constants import Tasks


@PIPELINES.register_module(
    Tasks.shop_segmentation, module_name=Pipelines.shop_segmentation)
class ShopSegmentationPipeline(Pipeline):

    def __init__(self, model: str, **kwargs):
        """
            model: model id on modelscope hub.
        """
        super().__init__(model=model, auto_collate=False, **kwargs)

    def preprocess(self, input: Input) -> Dict[str, Any]:
        img = LoadImage.convert_to_ndarray(input)
        img_tensor, ori_h, ori_w, crop_h, crop_w = self.model.preprocess(img)
        result = {
            'img': img_tensor,
            'ori_h': ori_h,
            'ori_w': ori_w,
            'crop_h': crop_h,
            'crop_w': crop_w
        }
        return result

    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:

        outputs = self.model.inference(input['img'])
        result = {
            'data': outputs,
            'ori_h': input['ori_h'],
            'ori_w': input['ori_w'],
            'crop_h': input['crop_h'],
            'crop_w': input['crop_w'],
        }
        return result

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:

        data = self.model.postprocess(inputs['data'], inputs['crop_h'],
                                      inputs['crop_w'], inputs['ori_h'],
                                      inputs['ori_w'])
        outputs = {OutputKeys.MASKS: data}
        return outputs
