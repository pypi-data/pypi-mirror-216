import os
from typing import Dict

import torch
from torch import nn

from weathon.base import TorchModel
from weathon.registry import MODELS
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models
from weathon.utils.typing import Tensor
# from weathon.base import BaseModel, Tensor, TorchModel
# from weathon.registry import MODELS
# from weathon.utils.config.config import Config
# from weathon.utils.constants import ModelFile, Tasks
from .backbone import ClassifyRerank


@MODELS.register_module(Tasks.document_grounded_dialog_rerank, module_name=Models.doc2bot)
class DocumentGroundedDialogRerankModel(TorchModel):
    _backbone_prefix = ''

    def __init__(self, model_dir, **kwargs):
        super().__init__(model_dir, **kwargs)
        self.model = ClassifyRerank(model_dir)

    def forward(self, input: Dict[str, Tensor]):
        outputs = self.model(
            input_ids=input['input_ids'],
            attention_mask=input['attention_mask'])
        return outputs

    def resize_token_embeddings(self, size):
        self.model.base_model.resize_token_embeddings(size)

    def save_pretrained(self, addr):
        self.model.base_model.save_pretrained(addr)
