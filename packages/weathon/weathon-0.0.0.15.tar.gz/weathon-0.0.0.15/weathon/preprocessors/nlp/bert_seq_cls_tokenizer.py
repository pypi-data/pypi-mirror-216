from typing import Any, Dict, Union

from transformers import AutoTokenizer

from weathon.base import BasePreprocessor
from weathon.registry import PREPROCESSORS
from weathon.utils.constants import Fields, InputFields


@PREPROCESSORS.register_module(Fields.nlp)
class Tokenize(BasePreprocessor):

    def __init__(self, tokenizer_name) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def __call__(self, data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(data, str):
            data = {InputFields.text: data}
        token_dict = self.tokenizer(data[InputFields.text])
        data.update(token_dict)
        return data
