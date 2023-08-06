from transformers import GPTNeoConfig
from transformers import GPTNeoModel as GPTNeoModelTransform

from weathon.registry import BACKBONES
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models


@BACKBONES.register_module(group_key=Tasks.backbone, module_name=Models.gpt_neo)
class GPTNeoModel(GPTNeoModelTransform):

    def __init__(self, **kwargs):
        config = GPTNeoConfig(**kwargs)
        super().__init__(config)
