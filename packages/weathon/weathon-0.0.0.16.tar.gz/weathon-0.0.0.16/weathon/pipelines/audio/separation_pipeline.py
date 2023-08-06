import io
from typing import Any, Dict

import numpy
import soundfile as sf
import torch

from weathon.base import BasePipeline
from weathon.utils.constants.metainfo import Pipelines
from weathon.registry import PIPELINES
from weathon.utils.constants import Tasks
from weathon.utils.constants.output_constant import OutputKeys
from weathon.utils.fileio import File
from weathon.utils.logger import get_logger
from weathon.utils.typing import Input

logger = get_logger()


@PIPELINES.register_module(Tasks.speech_separation, module_name=Pipelines.speech_separation)
class SeparationPipeline(BasePipeline):

    def __init__(self, model, **kwargs):
        """create a speech separation pipeline for prediction

        Args:
            model: model id on modelscope hub.
        """
        logger.info('loading model...')
        super().__init__(model=model, **kwargs)
        self.model.load_check_point(device=self.device)
        self.model.eval()

    def preprocess(self, inputs: Input, **preprocess_params) -> Dict[str, Any]:
        if isinstance(inputs, str):
            file_bytes = File.read(inputs)
            data, fs = sf.read(io.BytesIO(file_bytes), dtype='float32')
            if fs != 8000:
                raise ValueError(
                    'modelscope error: The audio sample rate should be 8000')
        elif isinstance(inputs, bytes):
            data = torch.from_numpy(
                numpy.frombuffer(inputs, dtype=numpy.float32))
        return dict(data=data)

    def postprocess(self, inputs: Dict[str, Any],
                    **post_params) -> Dict[str, Any]:
        return inputs

    def forward(
        self, inputs: Dict[str, Any], **forward_params
    ) -> Dict[str, Any]:  # mix, targets, stage, noise=None):
        """Forward computations from the mixture to the separated signals."""
        logger.info('Start forward...')
        # Unpack lists and put tensors in the right device
        mix = inputs['data'].to(self.device)
        mix = torch.unsqueeze(mix, dim=1).transpose(0, 1)
        est_source = self.model(mix)
        result = []
        for ns in range(self.model.num_spks):
            signal = est_source[0, :, ns]
            signal = signal / signal.abs().max() * 0.5
            signal = signal.unsqueeze(0).cpu()
            # convert tensor to pcm
            output = (signal.numpy() * 32768).astype(numpy.int16).tobytes()
            result.append(output)
        logger.info('Finish forward.')
        return {OutputKeys.OUTPUT_PCM_LIST: result}
