from typing import Optional, Union

from weathon.utils.constants.metainfo import Pipelines
from weathon.models import Model
from weathon.registry import PIPELINES
from weathon.pipelines.nlp import TokenClassificationPipeline
from weathon.preprocessors import Preprocessor
from weathon.utils.constants import ModelFile, Tasks

__all__ = ['NamedEntityRecognitionPipeline']


@PIPELINES.register_module(
    Tasks.named_entity_recognition,
    module_name=Pipelines.named_entity_recognition)
@PIPELINES.register_module(
    Tasks.named_entity_recognition,
    module_name=Pipelines.named_entity_recognition_thai)
@PIPELINES.register_module(
    Tasks.named_entity_recognition,
    module_name=Pipelines.named_entity_recognition_viet)
class NamedEntityRecognitionPipeline(TokenClassificationPipeline):

    def __init__(self,
                 model: Union[Model, str],
                 preprocessor: Optional[Preprocessor] = None,
                 config_file: str = None,
                 device: str = 'gpu',
                 auto_collate=True,
                 sequence_length=512,
                 **kwargs):
        """Use `model` and `preprocessor` to create a nlp NER pipeline for prediction

        Args:
            model (str or Model): Supply either a local model dir which supported NER task, or a
            model id from the model hub, or a torch model instance.
            preprocessor (BasePreprocessor): An optional preprocessor instance, please make sure the preprocessor fits for
                the model if supplied.
            kwargs (dict, `optional`):
                Extra kwargs passed into the preprocessor's constructor.

        Examples:
            >>> from weathon.pipelines import pipeline
            >>> pipeline_ins = pipeline(task='named-entity-recognition',
            >>>        model='damo/nlp_raner_named-entity-recognition_chinese-base-news')
            >>> input = '这与温岭市新河镇的一个神秘的传说有关。'
            >>> print(pipeline_ins(input))

            To view other examples plese check the tests/pipelines/test_plugin_model.py.
        """
        super().__init__(
            model=model,
            preprocessor=preprocessor,
            config_file=config_file,
            device=device,
            auto_collate=auto_collate,
            compile=kwargs.pop('compile', False),
            compile_options=kwargs.pop('compile_options', {}))

        assert isinstance(self.model, Model), \
            f'please check whether model config exists in {ModelFile.CONFIGURATION}'

        if preprocessor is None:
            self.preprocessor = Preprocessor.from_pretrained(
                self.model.model_dir,
                sequence_length=sequence_length,
                **kwargs)
        self.model.eval()
        assert hasattr(self.preprocessor, 'id2label')
        self.id2label = self.preprocessor.id2label
