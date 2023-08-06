import os
from typing import Any, Dict

from weathon.base import BaseModel
from weathon.registry import MODELS
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models
# from weathon.base import BaseModel
# from weathon.registry import MODELS
# from weathon.utils.constants import Tasks

__all__ = ['GenericKeyWordSpotting']


@MODELS.register_module(Tasks.keyword_spotting, module_name=Models.kws_kwsbp)
class GenericKeyWordSpotting(BaseModel):

    def __init__(self, model_dir: str, *args, **kwargs):
        """initialize the info of model.

        Args:
            model_dir (str): the model path.
        """
        super().__init__(model_dir, *args, **kwargs)
        self.model_cfg = {
            'model_workspace': model_dir,
            'config_path': os.path.join(model_dir, 'config.yaml')
        }

    def forward(self) -> Dict[str, Any]:
        """return the info of the model
        """
        return self.model_cfg
