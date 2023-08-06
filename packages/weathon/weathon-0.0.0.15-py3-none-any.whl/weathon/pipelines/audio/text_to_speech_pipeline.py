from typing import Any, Dict

import numpy as np

from weathon.base import BasePipeline
from weathon.base.pipeline import InputModel, Input
from weathon.utils.constants.metainfo import Pipelines
from weathon.models.audio.tts import SambertHifigan
from weathon.registry import PIPELINES
from weathon.utils.constants import Tasks

__all__ = ['TextToSpeechSambertHifiganPipeline']

from weathon.utils.constants.output_constant import OutputKeys


@PIPELINES.register_module(
    Tasks.text_to_speech, module_name=Pipelines.sambert_hifigan_tts)
class TextToSpeechSambertHifiganPipeline(BasePipeline):

    def __init__(self, model: InputModel, **kwargs):
        """use `model` to create a text-to-speech pipeline for prediction

        Args:
            model (SambertHifigan or str): a model instance or valid offical model id
        """
        super().__init__(model=model, **kwargs)

    def forward(self, input: str, **forward_params) -> Dict[str, bytes]:
        """synthesis text from inputs with pipeline
        Args:
            input (str): text to synthesis
            forward_params: valid param is 'voice' used to setting speaker vocie
        Returns:
            Dict[str, np.ndarray]: {OutputKeys.OUTPUT_PCM : np.ndarray(16bit pcm data)}
        """
        output_wav = self.model.forward(input, forward_params.get('voice'))
        return {OutputKeys.OUTPUT_WAV: output_wav}

    def postprocess(self, inputs: Dict[str, Any],
                    **postprocess_params) -> Dict[str, Any]:
        return inputs

    def preprocess(self, inputs: Input, **preprocess_params) -> Dict[str, Any]:
        return inputs

    def _sanitize_parameters(self, **pipeline_parameters):
        return {}, pipeline_parameters, {}
