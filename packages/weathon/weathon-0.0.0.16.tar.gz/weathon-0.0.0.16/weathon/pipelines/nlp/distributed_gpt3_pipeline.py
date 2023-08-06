from typing import Any, Dict

import torch

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.nlp import DistributedGPT3
from weathon.pipelines.base import DistributedPipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import TextGenerationJiebaPreprocessor
from weathon.utils.constants import Tasks


@PIPELINES.register_module(
    Tasks.text_generation, module_name=Pipelines.gpt3_generation)
class DistributedGPT3Pipeline(DistributedPipeline):
    """This class is used to instantiate the gpt3 model.
    """

    model = None

    def __init__(self, model, preprocessor=None, **kwargs):
        """

        Args:
            model: The model piece, str is not supported.
            preprocessor: The preprocessor matched with the model.
            kwargs (dict, `optional`):
                Extra kwargs passed into the preprocessor's constructor.
        """
        if preprocessor is None:
            preprocessor = TextGenerationJiebaPreprocessor(model)
        super().__init__(model, preprocessor=preprocessor, **kwargs)
        assert hasattr(preprocessor, 'tokenizer')

    @classmethod
    def _instantiate_one(cls, rank, model_dir, **kwargs):
        cls.model = DistributedGPT3(model_dir, rank, **kwargs)
        cls.model.eval()

    @classmethod
    def _forward_one(cls, inputs: Dict[str, Any]) -> Dict[str, Any]:
        tokens = inputs['inputs']['input_ids'].cuda(
            torch.cuda.current_device())
        return cls.model.generate(tokens, **inputs['forward_params'])

    def postprocess(self, inputs: Dict[str, Any],
                    **postprocess_params) -> Dict[str, str]:
        """process the prediction results

        Args:
            inputs (Dict[str, Any]): _description_

        Returns:
            Dict[str, str]: the prediction results
        """
        from weathon.outputs import OutputKeys
        return {
            OutputKeys.TEXT:
            self.preprocessor.tokenizer.detokenize(
                inputs.sequences[0].tolist())
        }

    def _sanitize_parameters(self, **pipeline_parameters):
        return {}, pipeline_parameters, {}
