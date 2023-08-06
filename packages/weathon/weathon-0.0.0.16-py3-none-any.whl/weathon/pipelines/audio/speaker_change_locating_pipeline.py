import io
from typing import Any, Dict, List, Union

import numpy as np
import soundfile as sf
import torch

from weathon.base import BasePipeline
from weathon.base.pipeline import InputModel
from weathon.utils.constants.metainfo import Pipelines
from weathon.registry import PIPELINES
from weathon.utils.constants import Tasks
from weathon.utils.constants.output_constant import OutputKeys
from weathon.utils.fileio import File
from weathon.utils.logger import get_logger

logger = get_logger()

__all__ = ['SpeakerChangeLocatingPipeline']


@PIPELINES.register_module(
    Tasks.speaker_diarization, module_name=Pipelines.speaker_change_locating)
class SpeakerChangeLocatingPipeline(BasePipeline):
    """Speaker Change Locating Inference Pipeline
    use `model` to create a speaker change Locating pipeline.

    Args:
        model (SpeakerChangeLocatingPipeline): A model instance, or a model local dir, or a model id in the model hub.
        kwargs (dict, `optional`):
            Extra kwargs passed into the pipeline's constructor.
    Example:
    >>> from weathon.pipelines import pipeline
    >>> from weathon.utils.constants import Tasks
    >>> p = pipeline(
    >>>    task=Tasks.speaker_diarization, model='damo/speech_campplus-transformer_scl_zh-cn_16k-common')
    >>> print(p(audio))

    """

    def __init__(self, model: InputModel, **kwargs):
        """use `model` to create a speaker change Locating pipeline for prediction
        Args:
            model (str): a valid offical model id
        """
        super().__init__(model=model, **kwargs)
        self.model_config = self.model.model_config
        self.config = self.model.model_config
        self.anchor_size = self.config['anchor_size']

    def __call__(self, audio: str, embds: List = None) -> Dict[str, Any]:
        if embds is not None:
            assert len(embds) == 2
            assert isinstance(embds[0], np.ndarray) and isinstance(
                embds[1], np.ndarray)
            assert embds[0].shape == (
                self.anchor_size, ) and embds[1].shape == (self.anchor_size, )
        else:
            embd1 = np.zeros(self.anchor_size // 2)
            embd2 = np.ones(self.anchor_size - self.anchor_size // 2)
            embd3 = np.ones(self.anchor_size // 2)
            embd4 = np.zeros(self.anchor_size - self.anchor_size // 2)
            embds = [
                np.stack([embd1, embd2], axis=1).flatten(),
                np.stack([embd3, embd4], axis=1).flatten(),
            ]
        anchors = torch.from_numpy(np.stack(embds,
                                            axis=0)).float().unsqueeze(0)

        output = self.preprocess(audio)
        output = self.forward(output, anchors)
        output = self.postprocess(output)

        return output

    def forward(self, input: torch.Tensor, anchors: torch.Tensor):
        output = self.model(input, anchors)
        return output

    def postprocess(self, input: torch.Tensor) -> Dict[str, Any]:
        predict = np.where(np.diff(input.argmax(-1).numpy()))
        try:
            predict = predict[0][0] * 0.01 + 0.02
            predict = round(predict, 2)
            return {OutputKeys.TEXT: f'The change point is at {predict}s.'}
        except Exception:
            return {OutputKeys.TEXT: 'No change point is found.'}

    def preprocess(self, input: str) -> torch.Tensor:
        if isinstance(input, str):
            file_bytes = File.read(input)
            data, fs = sf.read(io.BytesIO(file_bytes), dtype='float32')
            if len(data.shape) == 2:
                data = data[:, 0]
            if fs != self.model_config['sample_rate']:
                raise ValueError(
                    'modelscope error: Only support %d sample rate files'
                    % self.model_cfg['sample_rate'])
            data = torch.from_numpy(data).unsqueeze(0)
        else:
            raise ValueError(
                'modelscope error: The input type is restricted to audio file address'
                % i)
        return data
