from weathon.registry import MODELS
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Heads, Models
from weathon.models.nlp.task_models.fill_mask import ModelForFillMask
from weathon.utils import logger as logging

logger = logging.get_logger()


@MODELS.register_module(Tasks.fill_mask, module_name=Models.bert)
class BertForMaskedLM(ModelForFillMask):

    base_model_type = Models.bert
    head_type = Heads.bert_mlm
