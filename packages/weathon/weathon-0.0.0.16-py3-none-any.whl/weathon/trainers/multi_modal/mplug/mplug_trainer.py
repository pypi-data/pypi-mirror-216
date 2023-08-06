from collections.abc import Mapping
from typing import Optional, Union

import torch
from torch import nn

from weathon.registry import TRAINERS
from weathon.utils.constants.metainfo import Trainers
from weathon.base import TorchModel, EpochBasedTrainer, BaseModel
from weathon.utils.constants.output_constant import OutputKeys
from weathon.utils.fileio.file_utils import func_receive_dict_inputs


@TRAINERS.register_module(module_name=Trainers.mplug)
class MPlugTrainer(EpochBasedTrainer):

    def __init__(self, *args, **kwargs):
        self.task: Optional[str] = kwargs.pop('task', None)
        super().__init__(*args, **kwargs)

    def build_model(self) -> Union[nn.Module, TorchModel]:
        return BaseModel.from_pretrained(
            self.model_dir, task=self.task, cfg_dict=self.cfg)

    def _decode(self, tokens):
        tokenizer = self.eval_preprocessor.tokenizer
        return tokenizer.decode(tokens, skip_special_tokens=True)

    def evaluation_step(self, data):
        model = self.model.module if self._dist else self.model
        model.eval()

        with torch.no_grad():
            if isinstance(
                    data,
                    Mapping) and not func_receive_dict_inputs(model.forward):
                result = model.forward(**data)
            else:
                result = model.forward(data)

        result[OutputKeys.TEXT] = [
            self._decode(seq) for seq in result['sequences']
        ]
        data[OutputKeys.LABELS] = [
            self._decode(seq) for seq in data['answer_input_ids']
        ]

        return result
