from weathon.registry import MODELS
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models
from weathon.models.nlp import ModelForTextClassification
from weathon.utils import logger as logging

logger = logging.get_logger()


@MODELS.register_module(Tasks.text_classification, module_name=Models.bert)
@MODELS.register_module(Tasks.nli, module_name=Models.bert)
@MODELS.register_module(Tasks.sentiment_classification, module_name=Models.bert)
@MODELS.register_module(Tasks.sentence_similarity, module_name=Models.bert)
@MODELS.register_module(Tasks.zero_shot_classification, module_name=Models.bert)
class BertForSequenceClassification(ModelForTextClassification):
    r"""Bert Model transformer with a sequence classification/regression head on top
    (a linear layer on top of the pooled output) e.g. for GLUE tasks.

    This model inherits from :class:`SequenceClassificationModel`. Check the superclass documentation for the generic
    methods the library implements for all its model (such as downloading or saving, resizing the input embeddings,
    pruning heads etc.)

    This model is also a PyTorch `torch.nn.Module <https://pytorch.org/docs/stable/nn.html#torch.nn.Module>`__
    subclass. Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to
    general usage and behavior.
    """
    base_model_type = 'bert'
