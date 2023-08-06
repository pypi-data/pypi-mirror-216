from typing import Any, Dict, List, Tuple, Union

import numpy as np

from weathon.base import BasePreprocessor
from weathon.registry import PREPROCESSORS
from weathon.utils.config.config import Config
from weathon.utils.constants.metainfo import Preprocessors
from weathon.utils.logger import get_logger
from weathon.utils.preprocessor.transformers_tokenizer import NLPTokenizer
from weathon.utils.constants import ModeKeys, Fields, Tasks,Datasets
from weathon.utils.hub.utils import parse_label_mapping, get_model_type
from weathon.utils.preprocessor.preprocessor_utils import parse_text_and_label, labels_to_id

logger = get_logger()


class TextClassificationPreprocessorBase(BasePreprocessor):

    def __init__(
        self,
        model_dir=None,
        first_sequence: str = None,
        second_sequence: str = None,
        label: str = 'label',
        label2id: Dict = None,
        mode: str = ModeKeys.INFERENCE,
        keep_original_columns: List[str] = None,
    ):
        """文本分类预处理的基类

        Args:
            model_dir(str, `optional`): The model dir used to parse the label mapping, can be None.
            first_sequence(str, `optional`): The key of the first sequence.
            second_sequence(str, `optional`): The key of the second sequence.
            label(str, `optional`): The keys of the label columns, default is `label`
            label2id: (dict, `optional`): The optional label2id mapping
            mode(str, `optional`): The mode for the preprocessor
            keep_original_columns(List[str], `optional`): 当输入当input为dict类型时,保留哪些原始当列
        """
        super().__init__(mode)
        self.model_dir = model_dir
        self.first_sequence = first_sequence
        self.second_sequence = second_sequence
        self.label = label
        self.label2id = label2id
        self.keep_original_columns = keep_original_columns
        if self.label2id is None and self.model_dir is not None:
            self.label2id = parse_label_mapping(self.model_dir)

        logger.info(f'The key of sentence1: {self.first_sequence}, '
                    f'The key of sentence2: {self.second_sequence}, '
                    f'The key of label: {self.label}')
        if self.first_sequence is None:
            logger.warning('[Important] first_sequence attribute is not set, '
                           'this will cause an error if your input is a dict.')

    @property
    def id2label(self):
        """ 根据label2id映射返回id2label
        """
        return {id: label for label, id in self.label2id.items()} if self.label2id else None

    def __call__(self, data: Union[str, Tuple, Dict],
                 **kwargs) -> Dict[str, Any]:
        """process the raw input data

        Args:
            data (tuple): [sentence1, sentence2]
                sentence1 (str): a sentence
                sentence2 (str): a sentence

        Returns:
            Dict[str, Any]: the preprocessed data
        """

        text_a, text_b, labels = parse_text_and_label(data,
                                                      self.mode,
                                                      self.first_sequence,
                                                      self.second_sequence,
                                                      self.label)
        output = self._tokenize_text(text_a, text_b, **kwargs)
        output = { k: np.array(v) if isinstance(v, list) else v for k, v in output.items() }
        labels_to_id(labels, output, self.label2id)
        if self.keep_original_columns and isinstance(data, dict):
            for column in self.keep_original_columns:
                output[column] = data[column]
        return output

    def _tokenize_text(self, sequence1, sequence2=None, **kwargs):
        """Tokenize the text.

        Args:
            sequence1: The first sequence.
            sequence2: The second sequence which may be None.

        Returns:
            The encoded sequence.
        """
        raise NotImplementedError()

@PREPROCESSORS.register_module(group_key=Tasks.text_classification, module_name=Datasets.jd_sentiment_text_classification)
class JDTextClassificationPreprocessor(TextClassificationPreprocessorBase):

    def __init__(self, preprocessor_cfg: Config = None, *args, **kwargs):
        preprocessor_cfg = preprocessor_cfg if preprocessor_cfg else dict()
        
        self.model_dir = kwargs.get('model_dir', preprocessor_cfg.get('model_dir', None))
        self.sequence_length = kwargs.get('sequence_length',preprocessor_cfg.get('sequence_length', None))
        self.sequence_length = kwargs.get('sequence_length', preprocessor_cfg.get('sequence_length', 128))
        self.max_length = kwargs.get('max_length',preprocessor_cfg.get('max_length', self.sequence_length))
        self.truncation = kwargs.get('truncation', preprocessor_cfg.get('truncation', True))
        self.padding = kwargs.get('padding', preprocessor_cfg.get('padding', 'max_length'))
        self.use_fast = kwargs.get('use_fast', preprocessor_cfg.get('use_fast', False))
        self.first_sequence = kwargs.get('first_sequence', preprocessor_cfg.get('first_sequence', "sentence"))
        self.second_sequence = kwargs.get('second_sequence', preprocessor_cfg.get('second_sequence', None))
        self.label = kwargs.get('label', preprocessor_cfg.get('label',"label"))
        self.label2id = kwargs.get('label2id', preprocessor_cfg.get('label2id',None))
        self._mode = kwargs.get('mode', preprocessor_cfg.get('mode', ModeKeys.TRAIN))
        self.keep_original_columns = kwargs.get('keep_original_columns', preprocessor_cfg.get('keep_original_columns',[]))
        if self.label2id is None and self.model_dir is not None:
            self.label2id = parse_label_mapping(self.model_dir)

        tokenize_kwargs = dict(
            truncation=self.truncation,
            padding=self.padding,
            max_length=self.max_length
        )
        logger.info(f'The key of sentence1: {self.first_sequence}, '
                    f'The key of sentence2: {self.second_sequence}, '
                    f'The key of label: {self.label}')
        if self.first_sequence is None:
            logger.warning('[Important] first_sequence attribute is not set, '
                           'this will cause an error if your input is a dict.')

        model_type = None
        if self.model_dir is not None:
            model_type = get_model_type(self.model_dir)
        self.nlp_tokenizer = NLPTokenizer(self.model_dir, model_type, use_fast=self.use_fast, tokenize_kwargs=tokenize_kwargs)

    def _tokenize_text(self, sequence1, sequence2=None, **kwargs):
        if 'return_tensors' not in kwargs:
            kwargs['return_tensors'] = 'pt' if self.mode == ModeKeys.INFERENCE else None
        return self.nlp_tokenizer(sequence1, sequence2, **kwargs)





@PREPROCESSORS.register_module(Fields.nlp, module_name=Preprocessors.nli_tokenizer)
@PREPROCESSORS.register_module(Fields.nlp, module_name=Preprocessors.sen_sim_tokenizer)
@PREPROCESSORS.register_module(Fields.nlp, module_name=Preprocessors.bert_seq_cls_tokenizer)
@PREPROCESSORS.register_module(Fields.nlp, module_name=Preprocessors.sen_cls_tokenizer)
class TextClassificationTransformersPreprocessor(TextClassificationPreprocessorBase):

    def _tokenize_text(self, sequence1, sequence2=None, **kwargs):
        if 'return_tensors' not in kwargs:
            kwargs['return_tensors'] = 'pt' if self.mode == ModeKeys.INFERENCE else None
        return self.nlp_tokenizer(sequence1, sequence2, **kwargs)

    def __init__(self,
                 model_dir=None,
                 first_sequence: str = None,
                 second_sequence: str = None,
                 label: Union[str, List] = 'label',
                 label2id: Dict = None,
                 mode: str = ModeKeys.INFERENCE,
                 max_length: int = None,
                 use_fast: bool = None,
                 keep_original_columns=None,
                 **kwargs):
        """The tokenizer preprocessor used in sequence classification.

        Args:
            use_fast: Whether to use the fast tokenizer or not.
            max_length: The max sequence length which the model supported,
                will be passed into tokenizer as the 'max_length' param.
            **kwargs: Extra args input into the tokenizer's __call__ method.
        """
        kwargs['truncation'] = kwargs.get('truncation', True)
        kwargs['padding'] = kwargs.get('padding', 'max_length')
        kwargs['max_length'] = max_length if max_length else kwargs.get('sequence_length', 128)
        kwargs.pop('sequence_length', None)
        model_type = None
        if model_dir is not None:
            model_type = get_model_type(model_dir)
        self.nlp_tokenizer = NLPTokenizer(model_dir, model_type, use_fast=use_fast, tokenize_kwargs=kwargs)
        super().__init__(model_dir, first_sequence, second_sequence, label,label2id, mode, keep_original_columns)



