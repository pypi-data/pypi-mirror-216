from transformers import GPT2Config
from transformers import GPT2Model as GPT2ModelTransform

from weathon.registry import BACKBONES
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models


@BACKBONES.register_module(group_key=Tasks.backbone, module_name=Models.gpt2)
class GPT2Model(GPT2ModelTransform):

    def __init__(self, **kwargs):
        config = GPT2Config(**kwargs)
        super().__init__(config)
