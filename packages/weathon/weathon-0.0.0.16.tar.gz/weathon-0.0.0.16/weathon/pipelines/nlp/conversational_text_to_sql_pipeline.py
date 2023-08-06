from typing import Any, Dict, Union

from text2sql_lgesql.utils.example import Example

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.nlp import StarForTextToSql
from weathon.outputs import OutputKeys
from weathon.base import BasePipeline
from weathon.registry import PIPELINES
from weathon.preprocessors import ConversationalTextToSqlPreprocessor
from weathon.utils.constants import Tasks

__all__ = ['ConversationalTextToSqlPipeline']


@PIPELINES.register_module(
    Tasks.table_question_answering,
    module_name=Pipelines.conversational_text_to_sql)
class ConversationalTextToSqlPipeline(Pipeline):

    def __init__(self,
                 model: Union[StarForTextToSql, str],
                 preprocessor: ConversationalTextToSqlPreprocessor = None,
                 config_file: str = None,
                 device: str = 'gpu',
                 auto_collate=True,
                 **kwargs):
        """use `model` and `preprocessor` to create a conversational text-to-sql prediction pipeline

        Args:
            model (StarForTextToSql): A model instance
            preprocessor (ConversationalTextToSqlPreprocessor): A preprocessor instance
            kwargs (dict, `optional`):
                Extra kwargs passed into the preprocessor's constructor.
        """
        super().__init__(
            model=model,
            preprocessor=preprocessor,
            config_file=config_file,
            device=device,
            auto_collate=auto_collate)
        if preprocessor is None:
            self.preprocessor = ConversationalTextToSqlPreprocessor(
                self.model.model_dir, **kwargs)

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """process the prediction results

        Args:
            inputs (Dict[str, Any]): _description_

        Returns:
            Dict[str, str]: the prediction results
        """
        sql = Example.evaluator.obtain_sql(inputs['predict'][0], inputs['db'])
        result = {OutputKeys.OUTPUT: {OutputKeys.TEXT: sql}}
        return result

    def _collate_fn(self, data):
        return data
