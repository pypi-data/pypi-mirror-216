import math
from typing import Any, Dict

import torch
import torch.nn.functional as F
from numpy import ndarray
from PIL import Image
from torchvision import transforms

from weathon.utils.constants.metainfo import Preprocessors
from weathon.preprocessors import load_image
from weathon.base import BasePreprocessor
from weathon.registry import PREPROCESSORS
from weathon.utils.constants import Fields
from weathon.utils.type_assert import type_assert


@PREPROCESSORS.register_module(
    Fields.cv,
    module_name=Preprocessors.image_quality_assessment_man_preprocessor)
class ImageQualityAssessmentMANPreprocessor(BasePreprocessor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transform_input = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
        ])

    @type_assert(object, object)
    def __call__(self, data) -> Dict[str, Any]:
        image = load_image(data)
        data = self.transform_input(image)
        data = data.unsqueeze(0)
        return {'input': data.float()}
