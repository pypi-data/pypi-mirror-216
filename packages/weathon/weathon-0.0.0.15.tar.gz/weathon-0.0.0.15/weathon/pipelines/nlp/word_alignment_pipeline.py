from typing import Any, Dict, Union

from weathon.utils.constants.metainfo import Pipelines
from weathon.models import Model
from weathon.outputs import OutputKeys
from weathon.base import BasePipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import WordAlignmentPreprocessor
from weathon.utils.constants import Tasks

__all__ = ['WordAlignmentPipeline']


@PIPELINES.register_module(
    Tasks.word_alignment, module_name=Pipelines.word_alignment)
class WordAlignmentPipeline(Pipeline):

    def __init__(self,
                 model: Union[Model, str],
                 preprocessor: WordAlignmentPreprocessor = None,
                 config_file: str = None,
                 device: str = 'gpu',
                 auto_collate=True,
                 sequence_length=128,
                 **kwargs):
        """Use `model` and `preprocessor` to create a nlp text dual encoder then generates the text representation.
        Args:
            model (str or Model): Supply either a local model dir which supported the WS task,
            or a model id from the model hub, or a torch model instance.
            preprocessor (BasePreprocessor): A WordAlignmentPreprocessor.
            kwargs (dict, `optional`):
                Extra kwargs passed into the preprocessor's constructor.
         Example:
            >>> from weathon.pipelines import pipeline
            >>> from weathon.utils.constants import Tasks
            >>> model_id = 'damo/Third-Party-Supervised-Word-Aligner-mBERT-base-zhen'
            >>> input = {"sentence_pair": '贝利 在 墨西哥 推出 自传 。||| pele promotes autobiography in mexico .'}
            >>> pipeline_ins = pipeline(Tasks.word_alignment, model=model_id)
            >>> print(pipeline_ins(input)['output'])
        """
        super().__init__(
            model=model,
            preprocessor=preprocessor,
            config_file=config_file,
            device=device,
            auto_collate=auto_collate)
        if preprocessor is None:
            self.preprocessor = WordAlignmentPreprocessor.from_pretrained(
                self.model.model_dir,
                sequence_length=sequence_length,
                **kwargs)

    def forward(self, inputs: Dict[str, Any],
                **forward_params) -> Dict[str, Any]:
        return self.model(**inputs, **forward_params)

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:

        align = []
        for k in inputs[0][0].keys():
            align.append(f'{k[0]}-{k[1]}')
        align = ' '.join(align)

        return {OutputKeys.OUTPUT: align}
