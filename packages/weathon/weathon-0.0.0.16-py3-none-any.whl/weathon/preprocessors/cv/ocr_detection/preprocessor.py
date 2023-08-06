
import math
import os

import cv2
import numpy as np
import PIL
import torch
from typing import Dict, Any


from weathon.preprocessors import load_image
from weathon.base import BasePreprocessor
from weathon.registry import PREPROCESSORS
from weathon.utils.config.config import Config
from weathon.utils.constants import Tasks,Datasets,ModeKeys, ModelFile,Fields
from weathon.utils.constants.metainfo import Preprocessors

from .transforms import AugmentData, AugmentDetectionData, MakeBorderMap, ICDARCollectFN, MakeICDARData, MakeSegDetectionData, NormalizeImage, RandomCropData


@PREPROCESSORS.register_module(group_key=Tasks.ocr_detection, module_name=Datasets.icdar2015_ocr_detection)
class Icdar2015Preprocessor(BasePreprocessor):

    def __init__(self, preprocessor_cfg: Config = None, *args, **kwargs):
        preprocessor_cfg = preprocessor_cfg if preprocessor_cfg else dict()

        self.transforms = kwargs.get("transforms", preprocessor_cfg.get("transforms", None))
        self._mode = kwargs.get('mode', preprocessor_cfg.get('mode', ModeKeys.TRAIN))
        self.is_training = (self._mode == ModeKeys.TRAIN)
    

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.transforms:
            return data

        if hasattr(self.transforms, 'detection_augment'):
            data_process0 = AugmentDetectionData(self.transforms.detection_augment)
            data = data_process0(data)

        # random crop augment
        if hasattr(self.transforms, 'random_crop'):
            data_process1 = RandomCropData(self.transforms.random_crop)
            data = data_process1(data)

        # data build in ICDAR format
        if hasattr(self.transforms, 'MakeICDARData'):
            data_process2 = MakeICDARData()
            data = data_process2(data)

        # Making binary mask from detection data with ICDAR format
        if hasattr(self.transforms, 'MakeSegDetectionData'):
            data_process3 = MakeSegDetectionData()
            data = data_process3(data)

        # Making the border map from detection data with ICDAR format
        if hasattr(self.transforms, 'MakeBorderMap'):
            data_process4 = MakeBorderMap()
            data = data_process4(data)

        # Image Normalization
        if hasattr(self.transforms, 'NormalizeImage'):
            data_process5 = NormalizeImage()
            data = data_process5(data)
        
        if self.is_training:
            # remove redundant data key for training
            for key in ['polygons', 'filename', 'shape', 'ignore_tags', 'is_training' ]:
                del data[key]
        return data






@PREPROCESSORS.register_module(Fields.cv, module_name=Preprocessors.ocr_detection)
class OCRDetectionPreprocessor(BasePreprocessor):

    def __init__(self, model_dir: str, mode: str = ModeKeys.INFERENCE):
        """The base constructor for all ocr recognition preprocessors.

        Args:
            model_dir (str): model directory to initialize some resource
            mode: The mode for the preprocessor.
        """
        super().__init__(mode)
        cfgs = Config.from_file(
            os.path.join(model_dir, ModelFile.CONFIGURATION))
        self.image_short_side = cfgs.model.inference_kwargs.image_short_side

    def __call__(self, inputs):
        """process the raw input data
        Args:
            inputs:
                - A string containing an HTTP link pointing to an image
                - A string containing a local path to an image
                - An image loaded in PIL(PIL.Image.Image) or opencv(np.ndarray) directly, 3 channels RGB
        Returns:
            outputs: the preprocessed image
        """
        if isinstance(inputs, str):
            img = np.array(load_image(inputs))
        elif isinstance(inputs, PIL.Image.Image):
            img = np.array(inputs)
        elif isinstance(inputs, np.ndarray):
            img = inputs
        else:
            raise TypeError(
                f'inputs should be either str, PIL.Image, np.array, but got {type(inputs)}'
            )

        img = img[:, :, ::-1]
        height, width, _ = img.shape
        if height < width:
            new_height = self.image_short_side
            new_width = int(math.ceil(new_height / height * width / 32) * 32)
        else:
            new_width = self.image_short_side
            new_height = int(math.ceil(new_width / width * height / 32) * 32)
        resized_img = cv2.resize(img, (new_width, new_height))
        resized_img = resized_img - np.array([123.68, 116.78, 103.94],
                                             dtype=np.float32)
        resized_img /= 255.
        resized_img = torch.from_numpy(resized_img).permute(
            2, 0, 1).float().unsqueeze(0)

        result = {'img': resized_img, 'org_shape': [height, width]}
        return result
