from typing import Union, Mapping, Optional, List, Tuple

from datasets import Dataset
from torch import nn

from weathon.base import EpochBasedTrainer, TorchModel, BasePreprocessor
from weathon.dataloader.cv.ocr_detection import OcrDetectionDataLoader
from weathon.registry import TRAINERS, build_model, build_custom_dataset, build_preprocessor
from weathon.utils.config.config import Config
from weathon.utils.constants import Tasks, ModeKeys, Datasets
from weathon.utils.dataset.dataset import WtDataset



# @TRAINERS.register_module(group_key=Tasks.ocr_detection, module_name=Datasets.icdar2015_ocr_detection)
class OcrDetectionTrainer(EpochBasedTrainer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_model(self) -> Union[nn.Module, TorchModel]:
        model_cfg = self.cfg.model
        model = build_model(model_cfg, task_name=model_cfg.task)
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

    def get_dataloader(self):
        is_train = (self.mode == ModeKeys.TRAIN)
        return OcrDetectionDataLoader(self.train_dataset, self.cfg.train.dataloader, is_train=is_train, distributed=self.is_distributed)

    def get_eval_dataloader(self):
        is_train = (self.mode == ModeKeys.TRAIN)
        return OcrDetectionDataLoader(self.eval_dataset, self.cfg.evaluation.dataloader, is_train=is_train,distributed=self.is_distributed)

    # def build_optimizer(self, cfg: ConfigDict, default_args: dict = None):
    #     lr = default_args.get("lr", cfg.get("lr", 0.007))
    #     momentum = default_args.get("momentum", cfg.get("momentum", 0.9))
    #     weight_decay = default_args.get("weight_decay", cfg.get("weight_decay", 0.0001))
    #     bn_group, weight_group, bias_group = [], [], []
    #
    #     for k, v in self.model.named_modules():
    #         if hasattr(v, 'bias') and isinstance(v.bias, nn.Parameter):
    #             bias_group.append(v.bias)
    #         if isinstance(v, nn.BatchNorm2d) or 'bn' in k:
    #             bn_group.append(v.weight)
    #         elif hasattr(v, 'weight') and isinstance(v.weight, nn.Parameter):
    #             weight_group.append(v.weight)
    #
    #     optimizer = torch.optim.SGD(bn_group, lr=lr, momentum=momentum, nesterov=True)
    #     optimizer.add_param_group({
    #         'params': weight_group,
    #         'weight_decay': weight_decay
    #     })
    #     optimizer.add_param_group({'params': bias_group})
    #     return optimizer
    #
    # def build_lr_scheduler(self, cfg: ConfigDict, default_args: dict = None):
    #     pass