
from typing import Dict, Any

from weathon.base import BasePreprocessor
from weathon.utils.config.config import Config
from weathon.utils.constants import Tasks,Datasets,ModeKeys
from weathon.registry import PREPROCESSORS

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
