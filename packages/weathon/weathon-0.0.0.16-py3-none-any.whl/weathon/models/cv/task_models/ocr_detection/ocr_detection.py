import os
from typing import Any, Dict

import numpy as np
import torch
import torch.nn.functional as F

from weathon.base import TorchModel
from weathon.registry import MODELS
from weathon.utils.constants import Tasks, ModelFile,Datasets
from weathon.utils.constants.metainfo import Models
from weathon.utils.config.config import Config
from weathon.utils.logger import get_logger
from weathon.models.cv.heads.ocr_detection_head import DBModel, VLPTModel
from .utils import boxes_from_bitmap, polygons_from_bitmap

logger = get_logger()

@MODELS.register_module(Tasks.ocr_detection, module_name=Datasets.icdar2015_ocr_detection)
@MODELS.register_module(Tasks.ocr_detection, module_name=Models.ocr_detection)
class OCRDetection(TorchModel):

    def __init__(self, model_dir: str, **kwargs):
        """initialize the ocr recognition model from the `model_dir` path.

        Args:
            model_dir (str): the model path.
        """
        super().__init__(model_dir, **kwargs)

        model_path = os.path.join(model_dir, ModelFile.TORCH_MODEL_FILE)
        cfgs = Config.from_file(os.path.join(model_dir, ModelFile.CONFIGURATION))
        self.thresh = cfgs.model.inference_kwargs.thresh
        self.return_polygon = cfgs.model.inference_kwargs.return_polygon
        self.backbone = cfgs.model.backbone
        self.detector = None
        if self.backbone == 'resnet50':
            self.detector = VLPTModel()
        elif self.backbone == 'resnet18':
            self.detector = DBModel()
        else:
            raise TypeError(f'detector backbone should be either resnet18, resnet50, but got {cfgs.model.backbone}')
        if model_path != '':
            self.detector.load_state_dict(torch.load(model_path, map_location='cpu'), strict=False)

    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            img (`torch.Tensor`): image tensor,
                shape of each tensor is [3, H, W].

        Return:
            results (`torch.Tensor`): bitmap tensor,
                shape of each tensor is [1, H, W].
            org_shape (`List`): image original shape,
                value is [height, width].
        """
        pred = self.detector(input['image'])
        return {'results': pred, 'org_shape': input['image'].shape}

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        pred = inputs['results'][0]
        height, width = inputs['org_shape']
        segmentation = pred > self.thresh
        if self.return_polygon:
            boxes, scores = polygons_from_bitmap(pred, segmentation, width,height)
        else:
            boxes, scores = boxes_from_bitmap(pred, segmentation, width,height)
        result = {'det_polygons': np.array(boxes)}
        return result
