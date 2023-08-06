from typing import Any, Dict, Union

from weathon.utils.constants.metainfo import Pipelines
from weathon.models import Model
from weathon.outputs import OutputKeys
from weathon.base import BasePipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import Preprocessor
from weathon.utils.constants import ModelFile, Tasks

__all__ = ['FaqQuestionAnsweringPipeline']


@PIPELINES.register_module(
    Tasks.faq_question_answering, module_name=Pipelines.faq_question_answering)
class FaqQuestionAnsweringPipeline(Pipeline):

    def __init__(self,
                 model: Union[str, Model],
                 preprocessor: Preprocessor = None,
                 config_file: str = None,
                 device: str = 'gpu',
                 auto_collate=True,
                 **kwargs):
        """The faq question answering pipeline.

        Args:
            model (str or Model): A model instance or a model local dir or a model id in the model hub.
            preprocessor (Preprocessor, `optional`): a preprocessor instance
            kwargs (dict, `optional`):
                The preprocessor kwargs passed into the preprocessor's constructor.
        """
        super().__init__(
            model=model,
            preprocessor=preprocessor,
            config_file=config_file,
            device=device,
            auto_collate=auto_collate)
        assert isinstance(self.model, Model), \
            f'please check whether model config exists in {ModelFile.CONFIGURATION}'
        if preprocessor is None:
            self.preprocessor = Preprocessor.from_pretrained(
                self.model.model_dir, **kwargs)
        if hasattr(self.model, 'eval'):
            self.model.eval()

    def _sanitize_parameters(self, **pipeline_parameters):
        return pipeline_parameters, pipeline_parameters, pipeline_parameters

    def get_sentence_embedding(self, inputs, max_len=None):
        inputs = self.preprocessor.batch_encode(inputs, max_length=max_len)
        sentence_vecs = self.model.forward_sentence_embedding(inputs)
        sentence_vecs = sentence_vecs.detach().tolist()
        return sentence_vecs

    def forward(self, inputs: Union[list, Dict[str, Any]],
                **forward_params) -> Dict[str, Any]:
        return self.model(inputs)

    def postprocess(self, inputs: Union[list, Dict[str, Any]],
                    **postprocess_params) -> Dict[str, Any]:
        scores = inputs['scores']
        labels = []
        for item in scores:
            tmplabels = [
                self.preprocessor.get_label(label_id)
                for label_id in range(len(item))
            ]
            labels.append(tmplabels)

        predictions = []
        for tmp_scores, tmp_labels in zip(scores.tolist(), labels):
            prediction = []
            for score, label in zip(tmp_scores, tmp_labels):
                prediction.append({
                    OutputKeys.LABEL: label,
                    OutputKeys.SCORE: score
                })
            predictions.append(
                list(
                    sorted(
                        prediction,
                        key=lambda d: d[OutputKeys.SCORE],
                        reverse=True)))

        return {OutputKeys.OUTPUT: predictions}
