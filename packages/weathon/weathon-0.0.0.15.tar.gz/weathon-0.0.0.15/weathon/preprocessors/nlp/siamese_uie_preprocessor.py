from typing import Any, Dict

from transformers import AutoTokenizer

from weathon.utils.constants.metainfo import Preprocessors
from weathon.preprocessors import Preprocessor
from weathon.registry import PREPROCESSORS
from weathon.utils.constants import Fields, ModeKeys


@PREPROCESSORS.register_module(
    Fields.nlp, module_name=Preprocessors.siamese_uie_preprocessor)
class SiameseUiePreprocessor(BasePreprocessor):
    """The tokenizer preprocessor used in zero shot classification.
    """

    def __init__(
        self,
        model_dir: str,
        mode: str = ModeKeys.INFERENCE,
        **kwargs,
    ):
        """preprocess the data
        Args:
            model_dir (str): model path
        """
        super().__init__(mode)
        self.model_dir: str = model_dir
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_dir, use_fast=True)

    def __call__(self, data: list, **kwargs) -> Dict[str, Any]:
        """process the raw input data

        Args:
            data (str or dict): a sentence
                Example:
                    'you are so handsome.'

        Returns:
            Dict[str, Any]: the preprocessed data
        """
        features = self.tokenizer(data, **kwargs)
        return features
