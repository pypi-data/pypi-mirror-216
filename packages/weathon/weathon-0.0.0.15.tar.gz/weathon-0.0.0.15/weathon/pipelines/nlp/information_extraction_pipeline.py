from typing import Any, Dict, Optional, Union

import torch

from weathon.utils.constants.metainfo import Pipelines
from weathon.models import Model
from weathon.base import BasePipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import Preprocessor
from weathon.utils.constants import ModelFile, Tasks

__all__ = ['InformationExtractionPipeline']


@PIPELINES.register_module(
    Tasks.information_extraction, module_name=Pipelines.relation_extraction)
@PIPELINES.register_module(
    Tasks.relation_extraction, module_name=Pipelines.relation_extraction)
class InformationExtractionPipeline(Pipeline):

    def __init__(self,
                 model: Union[Model, str],
                 preprocessor: Optional[Preprocessor] = None,
                 config_file: str = None,
                 device: str = 'gpu',
                 auto_collate=True,
                 sequence_length=512,
                 **kwargs):
        """

        Args:
            model (str or Model): Supply either a local model dir which supported information extraction task, or a
            model id from the model hub, or a torch model instance.
            preprocessor (BasePreprocessor): An optional preprocessor instance, please make sure the preprocessor fits for
            the model if supplied.
            kwargs (dict, `optional`):
                Extra kwargs passed into the preprocessor's constructor.
        """
        super().__init__(
            model=model,
            preprocessor=preprocessor,
            config_file=config_file,
            device=device,
            auto_collate=auto_collate)

        assert isinstance(self.model, Model), \
            f'please check whether model config exists in {ModelFile.CONFIGURATION}'

        if self.preprocessor is None:
            self.preprocessor = Preprocessor.from_pretrained(
                self.model.model_dir,
                sequence_length=sequence_length,
                **kwargs)
        self.model.eval()

    def forward(self, inputs: Dict[str, Any],
                **forward_params) -> Dict[str, Any]:
        with torch.no_grad():
            return self.model(**inputs, **forward_params)

    def postprocess(self, inputs: Dict[str, Any],
                    **postprocess_params) -> Dict[str, str]:
        return inputs
