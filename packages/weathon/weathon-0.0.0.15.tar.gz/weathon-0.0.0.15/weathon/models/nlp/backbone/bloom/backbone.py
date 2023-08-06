from transformers import BloomConfig
from transformers import BloomModel as BloomModelTransform

from weathon.registry import BACKBONES
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models


@BACKBONES.register_module(group_key=Tasks.backbone, module_name=Models.bloom)
class BloomModel(BloomModelTransform):

    def __init__(self, **kwargs):
        config = BloomConfig(**kwargs)
        super().__init__(config)
