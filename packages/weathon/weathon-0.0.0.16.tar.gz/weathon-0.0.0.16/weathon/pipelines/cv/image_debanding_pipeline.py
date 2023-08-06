from typing import Any, Dict, Optional, Union

import torch
from torchvision import transforms

from weathon.utils.constants.metainfo import Pipelines
from weathon.base import BaseModel
from weathon.models.cv.image_debanding import RRDBImageDebanding
from weathon.outputs import OutputKeys
from weathon.pipelines.base import Input, Pipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import LoadImage
from weathon.utils.constants import Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.image_debanding, module_name=Pipelines.image_debanding)
class ImageDebandingPipeline(Pipeline):

    def __init__(self, model: Union[RRDBImageDebanding, str], **kwargs):
        """The inference pipeline for image debanding.

        Args:
            model (`str` or `Model` or module instance): A model instance or a model local dir
                or a model id in the model hub.
            preprocessor (`Preprocessor`, `optional`): A Preprocessor instance.
            kwargs (dict, `optional`):
                Extra kwargs passed into the preprocessor's constructor.

        Example:
            >>> import cv2
            >>> from weathon.outputs import OutputKeys
            >>> from weathon.pipelines import pipeline
            >>> from weathon.utils.constants import Tasks
            >>> debanding = pipeline(Tasks.image_debanding, model='damo/cv_rrdb_image-debanding')
                result = debanding(
                    'https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/debanding.png')
            >>> cv2.imwrite('result.png', result[OutputKeys.OUTPUT_IMG])
        """
        super().__init__(model=model, **kwargs)
        self.model.eval()

        if torch.cuda.is_available():
            self._device = torch.device('cuda')
        else:
            self._device = torch.device('cpu')

    def preprocess(self, input: Input) -> Dict[str, Any]:
        img = LoadImage.convert_to_img(input)
        test_transforms = transforms.Compose([transforms.ToTensor()])
        img = test_transforms(img)
        result = {'src': img.unsqueeze(0).to(self._device)}
        return result

    @torch.no_grad()
    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:
        return super().forward(input)

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        output_img = (inputs['outputs'].squeeze(0) * 255.).type(
            torch.uint8).cpu().permute(1, 2, 0).numpy()[:, :, ::-1]
        return {OutputKeys.OUTPUT_IMG: output_img}
