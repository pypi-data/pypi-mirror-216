# Copyright (c) 2022 Zhipu.AI

import os.path as osp
import re
from typing import Any, Dict, Iterable, Optional, Tuple, Union

from weathon.utils.constants.metainfo import Models, Preprocessors
from weathon.outputs import OutputKeys
from weathon.base import BasePreprocessor
from weathon.registry import PREPROCESSORS
from weathon.utils.config.config import Config, ConfigFields
from weathon.utils.constants import Fields, InputFields, ModeKeys, ModelFile
from weathon.utils.hub import get_model_type, parse_label_mapping
from weathon.utils.logger import get_logger
from weathon.utils.nlp import import_external_nltk_data
from weathon.utils.type_assert import type_assert


@PREPROCESSORS.register_module(
    Fields.nlp, module_name=Preprocessors.mglm_summarization)
class MGLMSummarizationPreprocessor(BasePreprocessor):

    def __init__(self, *args, **kwargs):
        """preprocess the data
        Args:
            model_dir (str): model path
        """
        super().__init__(*args, **kwargs)

    @type_assert(object, (str, tuple, Dict))
    def __call__(self, data: Union[str, tuple, Dict]) -> Dict[str, Any]:
        return data
