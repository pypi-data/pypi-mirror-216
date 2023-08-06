from collections import OrderedDict
from typing import Dict

import torch
from transformers import BertTokenizer

from weathon.base import TorchModel
from weathon.registry import MODELS
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models
from weathon.models.nlp.gpt3 import GPT3Model

__all__ = ['GPT3ForTextGeneration']

from weathon.utils.hub.utils import read_config
from weathon.utils.typing import Tensor


@MODELS.register_module(Tasks.text_generation, module_name=Models.gpt3)
class GPT3ForTextGeneration(TorchModel):

    def __init__(self, model_dir: str, *args, **kwargs):
        """initialize the text generation model from the `model_dir` path.

        Args:
            model_dir (str): the model path.
        """
        super().__init__(model_dir, *args, **kwargs)

        # Temporarily compatible with DistributedGPT3 and GPT3Model,
        # the base/large model based on GPT3Model will be replaced in the future,
        # and GPT3Model will be deprecated
        if 'megatron' in read_config(model_dir):
            from weathon.models.nlp import DistributedGPT3
            self.model = DistributedGPT3(model_dir, **kwargs)
        else:
            self.model = GPT3Model.from_pretrained(model_dir)
            self.tokenizer = BertTokenizer.from_pretrained(model_dir)

    def forward(self, input: Dict[str, Tensor]) -> Dict[str, Tensor]:
        """return the result by the model

        Args:
            input (Dict[str, Tensor]): the preprocessed data

        Returns:
            Dict[str, Tensor]: results

        Example:
            >>> {
            >>>     'logits': Tensor([[0.54, 0.32...])]), # logits
            >>> }
        """
        return self.model(**input)

    def generate(self, inputs: Dict[str, Tensor],
                 **kwargs) -> Dict[str, Tensor]:
        if not isinstance(self.model, GPT3Model):
            return self.model.generate(**inputs, **kwargs)

        tokens = inputs['input_ids']
        lengths = self._get_length(inputs['attention_mask'])
        return self.model.generate(tokens, prompt_length=lengths, **kwargs)

    @staticmethod
    def _get_length(attention_mask: torch.Tensor) -> Tensor:
        return attention_mask.sum(-1) - 1

    def save_pretrained(self, *args, **kwargs):
        if not isinstance(self.model, GPT3Model):
            return self.model.save_pretrained(*args, **kwargs)
        return super().save_pretrained(*args, **kwargs)

    def state_dict(self, destination=None, prefix='', keep_vars=False):
        return self.model.state_dict(destination, prefix, keep_vars)

    def load_state_dict(self,
                        state_dict: 'OrderedDict[str, Tensor]',
                        strict: bool = True):
        return self.model.load_state_dict(state_dict, strict)
