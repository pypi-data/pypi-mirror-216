import math
import os
from typing import Any, Dict

import torch
import torchvision.transforms as T
from PIL import Image

from weathon.utils.constants.metainfo import Pipelines
from weathon.outputs import OutputKeys
from weathon.pipelines.base import Input, Pipeline
from weathon.registry import PIPELINES
from weathon.preprocessors.image import LoadImage
from weathon.utils.config.config import Config
from weathon.utils.constants import ModelFile, Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.image_reid_person, module_name=Pipelines.image_reid_person)
class ImageReidPersonPipeline(Pipeline):

    def __init__(self, model: str, **kwargs):
        """
            model: model id on modelscope hub.
        """
        assert isinstance(model, str), 'model must be a single str'
        super().__init__(model=model, auto_collate=False, **kwargs)
        logger.info(f'loading model config from dir {model}')

        cfg_path = os.path.join(model, ModelFile.CONFIGURATION)
        cfg = Config.from_file(cfg_path)
        cfg = cfg.model.cfg
        self.model = self.model.to(self.device)
        self.model.eval()

        self.val_transforms = T.Compose([
            T.Resize(cfg.INPUT.SIZE_TEST),
            T.ToTensor(),
            T.Normalize(mean=cfg.INPUT.PIXEL_MEAN, std=cfg.INPUT.PIXEL_STD)
        ])

    def preprocess(self, input: Input) -> Dict[str, Any]:
        img = LoadImage.convert_to_img(input)
        img = self.val_transforms(img)
        img = img.unsqueeze(0)
        img = img.to(self.device)
        return {'img': img}

    def forward(self, input: Dict[str, Any]) -> Dict[str, Any]:
        img = input['img']
        img_embedding = self.model(img)
        img_embedding = img_embedding.detach().cpu().numpy()
        return {OutputKeys.IMG_EMBEDDING: img_embedding}

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return inputs
