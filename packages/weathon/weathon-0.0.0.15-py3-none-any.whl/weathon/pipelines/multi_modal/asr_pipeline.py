from typing import Any, Dict, Optional, Union

import torch

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.multi_modal import MPlugForAllTasks, OfaForAllTasks
from weathon.pipelines.base import Model, Pipeline
from weathon.registry import PIPELINES
from weathon.pipelines.util import batch_process
from weathon.preprocessors import (MPlugPreprocessor, OfaPreprocessor,
                                      Preprocessor)
from weathon.utils.constants import Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.auto_speech_recognition, module_name=Pipelines.ofa_asr)
class AutomaticSpeechRecognitionPipeline(Pipeline):

    def __init__(self,
                 model: Union[Model, str],
                 preprocessor: Optional[Preprocessor] = None,
                 **kwargs):
        """
        use `model` and `preprocessor` to create an automatic speech recognition pipeline for prediction
        Args:
            model: model id on modelscope hub.
        """
        assert isinstance(model, str) or isinstance(model, Model), \
            'model must be a single str or OfaForAllTasks'
        if isinstance(model, str):
            pipe_model = Model.from_pretrained(model)
        elif isinstance(model, Model):
            pipe_model = model
        else:
            raise NotImplementedError
        pipe_model.model.eval()
        if preprocessor is None:
            if isinstance(pipe_model, OfaForAllTasks):
                preprocessor = OfaPreprocessor(pipe_model.model_dir)
            elif isinstance(pipe_model, MPlugForAllTasks):
                preprocessor = MPlugPreprocessor(pipe_model.model_dir)
        super().__init__(model=pipe_model, preprocessor=preprocessor, **kwargs)

    def _batch(self, data):
        if isinstance(self.model, OfaForAllTasks):
            return batch_process(self.model, data)
        else:
            return super(AutomaticSpeechRecognitionPipeline, self)._batch(data)

    def forward(self, inputs: Dict[str, Any],
                **forward_params) -> Dict[str, Any]:
        with torch.no_grad():
            return super().forward(inputs, **forward_params)

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return inputs
