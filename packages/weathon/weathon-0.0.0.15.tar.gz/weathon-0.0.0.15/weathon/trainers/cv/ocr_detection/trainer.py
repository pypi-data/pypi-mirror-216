from typing import Union, Mapping, Optional, List, Tuple

from datasets import Dataset
from torch import nn

from weathon.base import EpochBasedTrainer, TorchModel, BasePreprocessor
from weathon.registry import TRAINERS, build_model, build_custom_dataset, build_preprocessor
from weathon.utils.config.config import Config
from weathon.utils.constants import Tasks, ModeKeys, Datasets
from weathon.utils.dataset.dataset import WtDataset
from weathon.models.cv.ocr_detection.modules.dbnet import DBModel_v2
from weathon.utils.device import create_device


@TRAINERS.register_module(group_key=Tasks.ocr_detection, module_name=Datasets.icdar2015_ocr_detection)
class OcrDetectionTrainer(EpochBasedTrainer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_model(self) -> Union[nn.Module, TorchModel]:
        device = create_device("cpu")
        model = DBModel_v2(device)
        return model

    def get_preprocessors(self, preprocessor: Union[BasePreprocessor, Mapping, Config]) -> Tuple[
        BasePreprocessor, BasePreprocessor]:
        return self.build_preprocessor()

    def build_preprocessor(self) -> Tuple[BasePreprocessor, BasePreprocessor]:
        train_preprocessor_cfg = self.cfg.preprocessor.train
        eval_preprocessor_cfg = self.cfg.preprocessor.eval
        train_preprocessor = build_preprocessor(train_preprocessor_cfg, task_name=train_preprocessor_cfg.task)
        eval_preprocessor = build_preprocessor(eval_preprocessor_cfg, task_name=eval_preprocessor_cfg.task)
        train_preprocessor.mode = ModeKeys.TRAIN
        eval_preprocessor.mode = ModeKeys.EVAL
        return train_preprocessor, eval_preprocessor



    def build_dataset(self,
                      datasets: Union[Dataset, WtDataset, List[Dataset]],
                      cfg: Config,
                      mode: str,
                      preprocessor: Optional[BasePreprocessor] = None,
                      **kwargs):

        dataset_cfg = cfg.safe_get(f"dataset.{mode}")
        return build_custom_dataset(dataset_cfg, task_name=dataset_cfg.task, default_args=dict(preprocessor=preprocessor))
