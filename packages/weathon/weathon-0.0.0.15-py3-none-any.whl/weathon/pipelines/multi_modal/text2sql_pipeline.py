from typing import Any, Dict, Optional, Union

import torch

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.multi_modal import OfaForAllTasks
from weathon.pipelines.base import Model, Pipeline
from weathon.registry import PIPELINES
from weathon.pipelines.util import batch_process
from weathon.preprocessors import OfaPreprocessor, Preprocessor
from weathon.utils.constants import Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(Tasks.text2sql, module_name=Pipelines.ofa_text2sql)
class TextToSqlPipeline(Pipeline):
    R"""
    pipeline for text to sql task
    """

    def __init__(self,
                 model: Union[Model, str],
                 preprocessor: Optional[Preprocessor] = None,
                 **kwargs):
        """
        use `model` and `preprocessor` to create a pipeline for text2sql task
        Args:
            model: model id on modelscope hub.
        """
        super().__init__(model=model, preprocessor=preprocessor, **kwargs)
        self.model.eval()
        if preprocessor is None:
            if isinstance(self.model, OfaForAllTasks):
                self.preprocessor = OfaPreprocessor(self.model.model_dir)

    def _batch(self, data):
        if isinstance(self.model, OfaForAllTasks):
            return batch_process(self.model, data)
        else:
            return super(TextToSqlPipeline, self)._batch(data)

    def forward(self, inputs: Dict[str, Any],
                **forward_params) -> Dict[str, Any]:
        with torch.no_grad():
            return super().forward(inputs, **forward_params)

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return inputs
