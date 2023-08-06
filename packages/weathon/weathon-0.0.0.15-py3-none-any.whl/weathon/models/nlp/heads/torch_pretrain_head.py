from typing import Dict

import torch
from transformers.models.bert.modeling_bert import BertOnlyMLMHead
from transformers.models.roberta.modeling_roberta import RobertaLMHead

from weathon.base import TorchHead
from weathon.registry import HEADS
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Heads
# from weathon.models.base import TorchHead
# from weathon.models.builder import HEADS
# from weathon.utils.constants import Tasks


# @HEADS.register_module(Tasks.fill_mask, module_name=Heads.bert_mlm)
class BertMLMHead(BertOnlyMLMHead, TorchHead):

    def compute_loss(self, outputs: Dict[str, torch.Tensor],
                     labels) -> Dict[str, torch.Tensor]:
        raise NotImplementedError()


@HEADS.register_module(Tasks.fill_mask, module_name=Heads.roberta_mlm)
class RobertaMLMHead(RobertaLMHead, TorchHead):

    def compute_loss(self, outputs: Dict[str, torch.Tensor],
                     labels) -> Dict[str, torch.Tensor]:
        raise NotImplementedError()
