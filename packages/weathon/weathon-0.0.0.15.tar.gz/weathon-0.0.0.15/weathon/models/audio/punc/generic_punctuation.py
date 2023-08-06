import os
from typing import Any, Dict

from weathon.base import BaseModel
from weathon.registry import MODELS
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models
# from weathon.base import BaseModel
# from weathon.registry import MODELS
# from weathon.utils.constant import Frameworks, Tasks


@MODELS.register_module(Tasks.punctuation, module_name=Models.generic_punc)
class PunctuationProcessing(BaseModel):

    def __init__(self, model_dir: str, punc_model_name: str,
                 punc_model_config: Dict[str, Any], *args, **kwargs):
        """initialize the info of model.

        Args:
            model_dir (str): the model path.
            punc_model_name (str): the itn model name from configuration.json
            punc_model_config (Dict[str, Any]): the detail config about model from configuration.json
        """
        super().__init__(model_dir, punc_model_name, punc_model_config, *args,
                         **kwargs)
        self.model_cfg = {
            # the recognition model dir path
            'model_workspace': model_dir,
            # the itn model name
            'punc_model': punc_model_name,
            # the am model file path
            'punc_model_path': os.path.join(model_dir, punc_model_name),
            # the recognition model config dict
            'model_config': punc_model_config
        }

    def forward(self) -> Dict[str, Any]:
        """
          just return the model config

        """

        return self.model_cfg
