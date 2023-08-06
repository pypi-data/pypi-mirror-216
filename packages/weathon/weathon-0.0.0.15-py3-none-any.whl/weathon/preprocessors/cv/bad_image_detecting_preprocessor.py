from typing import Any, Dict

from numpy import ndarray
from PIL import Image
from torchvision import transforms

from weathon.base import BasePreprocessor
from weathon.registry import PREPROCESSORS
from weathon.utils.constants import Fields
from weathon.utils.constants.metainfo import Preprocessors
from weathon.utils.type_assert import type_assert


@PREPROCESSORS.register_module(Fields.cv, module_name=Preprocessors.bad_image_detecting_preprocessor)
class BadImageDetectingPreprocessor(BasePreprocessor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transform_input = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor()
        ])

    @type_assert(object, object)
    def __call__(self, data: ndarray) -> Dict[str, Any]:
        image = Image.fromarray(data)
        data = self.transform_input(image)
        data = data.unsqueeze(0)
        return {'input': data.float()}
