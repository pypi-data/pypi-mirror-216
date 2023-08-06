from typing import Any, Dict

import torch

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.nlp.gpt_moe.distributed_gpt_moe import DistributedGPTMoE
from weathon.pipelines.base import DistributedPipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import TextGenerationJiebaPreprocessor
from weathon.utils.constants import Tasks


@PIPELINES.register_module(
    Tasks.text_generation, module_name=Pipelines.gpt_moe_generation)
class DistributedGPTMoEPipeline(DistributedPipeline):
    """This class is used to instantiate the gpt-moe model.
    """

    model = None

    def __init__(self, model, preprocessor=None, **kwargs):
        if preprocessor is None:
            preprocessor = TextGenerationJiebaPreprocessor(model)
        super().__init__(model, preprocessor=preprocessor, **kwargs)
        assert hasattr(preprocessor, 'tokenizer')

    @classmethod
    def _instantiate_one(cls, rank, model_dir, **kwargs):
        cls.model = DistributedGPTMoE(model_dir, rank, **kwargs)
        cls.model.eval()

    @classmethod
    def _forward_one(cls, inputs: Dict[str, Any]) -> Dict[str, Any]:
        tokens = inputs['inputs']['input_ids'].cuda(
            torch.cuda.current_device())
        return cls.model.generate(tokens)

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
