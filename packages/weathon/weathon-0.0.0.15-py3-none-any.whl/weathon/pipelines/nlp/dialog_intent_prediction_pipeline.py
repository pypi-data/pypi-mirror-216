from typing import Any, Dict, Union

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.nlp import SpaceForDialogIntent
from weathon.outputs import OutputKeys
from weathon.base import BasePipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import DialogIntentPredictionPreprocessor
from weathon.utils.constants import Tasks

__all__ = ['DialogIntentPredictionPipeline']


@PIPELINES.register_module(
    Tasks.task_oriented_conversation,
    module_name=Pipelines.dialog_intent_prediction)
class DialogIntentPredictionPipeline(Pipeline):

    def __init__(self,
                 model: Union[SpaceForDialogIntent, str],
                 preprocessor: DialogIntentPredictionPreprocessor = None,
                 config_file: str = None,
                 device: str = 'gpu',
                 auto_collate=True,
                 **kwargs):
        """Use `model` and `preprocessor` to create a dialog intent prediction pipeline

        Args:
            model (str or SpaceForDialogIntent): Supply either a local model dir or a model id from the model hub,
            or a SpaceForDialogIntent instance.
            preprocessor (DialogIntentPredictionPreprocessor): An optional preprocessor instance.
            kwargs (dict, `optional`):
                Extra kwargs passed into the preprocessor's constructor.
        """
        super().__init__(
            model=model,
            preprocessor=preprocessor,
            config_file=config_file,
            device=device,
            auto_collate=auto_collate,
            compile=kwargs.pop('compile', False),
            compile_options=kwargs.pop('compile_options', {}))
        if preprocessor is None:
            self.preprocessor = DialogIntentPredictionPreprocessor(
                self.model.model_dir, **kwargs)
        self.categories = self.preprocessor.categories

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """process the prediction results

        Args:
            inputs (Dict[str, Any]): _description_

        Returns:
            Dict[str, str]: the prediction results
        """
        import numpy as np
        pred = inputs['pred']
        pos = np.where(pred == np.max(pred))

        return {
            OutputKeys.OUTPUT: {
                OutputKeys.PREDICTION: pred,
                OutputKeys.LABEL_POS: pos[0],
                OutputKeys.LABEL: self.categories[pos[0][0]]
            }
        }
