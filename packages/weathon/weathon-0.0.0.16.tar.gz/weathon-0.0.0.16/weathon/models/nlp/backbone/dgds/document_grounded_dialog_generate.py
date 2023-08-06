import os
from typing import Dict

import torch

from weathon.base import TorchModel
from weathon.registry import MODELS
from weathon.utils.config.config import Config
from weathon.utils.constants import Tasks, ModelFile
from weathon.utils.constants.metainfo import Models
from weathon.utils.typing import Tensor
# from weathon.utils.typing import Tensor, TorchModel
# from weathon.registry import MODELS
# from weathon.utils.config.config import Config
# from weathon.utils.constants import ModelFile, Tasks
from .backbone import Re2GModel


@MODELS.register_module(Tasks.document_grounded_dialog_generate, module_name=Models.doc2bot)
class DocumentGroundedDialogGenerateModel(TorchModel):
    _backbone_prefix = ''

    def __init__(self, model_dir, *args, **kwargs):
        super().__init__(model_dir, *args, **kwargs)
        self.config = Config.from_file(os.path.join(self.model_dir, ModelFile.CONFIGURATION))
        self.model = Re2GModel(model_dir, self.config)
        state_dict = torch.load(os.path.join(self.model_dir, ModelFile.TORCH_MODEL_BIN_FILE),map_location='cpu')
        self.model.load_state_dict(state_dict)

    def forward(self, input: Dict[str, Tensor]):
        rerank_input_ids = input['rerank_input_ids']
        input_ids = input['input_ids']
        attention_mask = input['attention_mask']
        label_ids = input['label_ids']

        outputs = self.model(rerank_input_ids, input_ids, attention_mask,
                             label_ids)
        return outputs

    def generate(self, input: Dict[str, Tensor]):
        rerank_input_ids = input['rerank_input_ids']
        input_ids = input['input_ids']
        attention_mask = input['attention_mask']
        outputs = self.model.generate(rerank_input_ids, input_ids,
                                      attention_mask)
        return outputs
