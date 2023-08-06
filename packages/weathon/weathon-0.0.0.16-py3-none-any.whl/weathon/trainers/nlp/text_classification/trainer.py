from typing import Union, Mapping, Optional, List, Tuple

from datasets import Dataset
from torch import nn

from weathon.base import EpochBasedTrainer, TorchModel, BasePreprocessor, BaseModel
from weathon.registry import TRAINERS, build_model, build_custom_dataset, build_preprocessor
from weathon.utils.constants import Tasks, ModeKeys, Datasets
from weathon.utils.dataset.dataset import WtDataset
from weathon.utils.config.config import Config


@TRAINERS.register_module(group_key=Tasks.text_classification, module_name=Datasets.jd_sentiment_text_classification)
class JDTextClassificationTrainer(EpochBasedTrainer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_model(self) -> Union[nn.Module, TorchModel]:
        """实例化pytorch模型.
        根据配置文件来构建模型
        """
        model_cfg = self.cfg.model
        model_args = dict(
            num_labels=model_cfg.num_labels,
            label2id=model_cfg.label2id,
            id2label=model_cfg.id2label
        )
        model = BaseModel.from_pretrained(self.model_dir, cfg_dict=self.cfg, **model_args)
        if not isinstance(model, nn.Module) and hasattr(model, 'model'):
            return model.model
        elif isinstance(model, nn.Module):
            return model

    def get_preprocessors(self, preprocessor: Union[BasePreprocessor, Mapping, Config]) -> Optional[BasePreprocessor]:
        return self.build_preprocessor()

    def build_preprocessor(self) -> Tuple[BasePreprocessor, BasePreprocessor]:
        train_preprocessor_cfg = self.cfg.preprocessor.train
        eval_preprocessor_cfg = self.cfg.preprocessor.eval
        train_preprocessor = build_preprocessor(train_preprocessor_cfg, task_name=train_preprocessor_cfg.task)
        train_preprocessor.mode = ModeKeys.TRAIN
        eval_preprocessor = build_preprocessor(eval_preprocessor_cfg, task_name=eval_preprocessor_cfg.task)
        eval_preprocessor.mode = ModeKeys.EVAL
        return train_preprocessor, eval_preprocessor

    def build_dataset(self, datasets: Union[Dataset, WtDataset, List[Dataset]], cfg: Config,
                      mode: str, preprocessor: Optional[BasePreprocessor] = None, **kwargs):
        dataset_cfg = self.cfg.safe_get(f"dataset.{mode}")
        return build_custom_dataset(dataset_cfg, task_name=dataset_cfg.task, default_args=dict(preprocessor=preprocessor))
