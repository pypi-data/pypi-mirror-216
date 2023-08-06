from typing import TYPE_CHECKING

from weathon.utils.import_utils import LazyImportModule

if TYPE_CHECKING:
    from .backbone.bart import BartForTextErrorCorrection
    from .backbone.bloom import BloomModel
    from .backbone.glm_130b import GLM130bForTextGeneration
    from .backbone.canmt import CanmtForTranslation
    from .backbone.deberta_v2 import DebertaV2ForMaskedLM, DebertaV2Model
    from .backbone.gpt_neo import GPTNeoModel
    from weathon.models.nlp.backbone.gpt2 import GPT2Model
    from .backbone.gpt3 import GPT3ForTextGeneration, DistributedGPT3
    from .backbone.gpt_moe import GPTMoEForTextGeneration, DistributedGPTMoE
    from .heads import TextClassificationHead
    from .backbone.hf_transformers import TransformersModel
    from .backbone.lstm import (
        LSTMModel,
        LSTMForTokenClassificationWithCRF,
    )
    from .backbone.mglm import MGLMForTextSummarization
    from weathon.models.nlp.backbone.palm_v2 import PalmForTextGeneration
    from .backbone.plug_mental import (PlugMentalConfig, PlugMentalModel,
                              PlugMentalForSequenceClassification)
    from .backbone.ponet import PoNetForMaskedLM, PoNetModel, PoNetConfig
    from .backbone.space_T_cn import TableQuestionAnswering
    from .backbone.space_T_en import StarForTextToSql
    from weathon.models.nlp.backbone.structbert import (
        SbertForFaqQuestionAnswering,
        SbertForMaskedLM,
        SbertForSequenceClassification,
        SbertForTokenClassification,
        SbertModel,
    )
    from .backbone.T5 import T5ForConditionalGeneration
    from .task_models import (
        ModelForFeatureExtraction,
        ModelForInformationExtraction,
        ModelForTextClassification,
        SingleBackboneTaskModelBase,
        ModelForTextGeneration,
        ModelForTextRanking,
        ModelForTokenClassification,
        ModelForTokenClassificationWithCRF,
    )
    from weathon.models.nlp.backbone.unite import UniTEForTranslationEvaluation
    from .backbone.use import UserSatisfactionEstimation
    from .backbone.llama import LlamaForTextGeneration, LlamaConfig, LlamaModel, LlamaTokenizer, LlamaTokenizerFast

else:
    _import_structure = {
        'bart': ['BartForTextErrorCorrection'],
        'bert': [
            'BertForMaskedLM',
            'BertForTextRanking',
            'BertForSentenceEmbedding',
            'BertForSequenceClassification',
            'BertForTokenClassification',
            'BertForDocumentSegmentation',
            'BertModel',
            'BertConfig',
            'SiameseUieModel',
        ],
        'bloom': ['BloomModel'],
        'csanmt': ['CsanmtForTranslation'],
        'canmt': ['CanmtForTranslation'],
        'codegeex':
        ['CodeGeeXForCodeTranslation', 'CodeGeeXForCodeGeneration'],
        'glm_130b': ['GLM130bForTextGeneration'],
        'deberta_v2': ['DebertaV2ForMaskedLM', 'DebertaV2Model'],
        'heads': ['TextClassificationHead'],
        'hf_transformers': ['TransformersModel'],
        'gpt2': ['GPT2Model'],
        'gpt3': ['GPT3ForTextGeneration', 'DistributedGPT3'],
        'gpt_moe': ['GPTMoEForTextGeneration', 'DistributedGPTMoE'],
        'gpt_neo': ['GPTNeoModel'],
        'structbert': [
            'SbertForFaqQuestionAnswering',
            'SbertForMaskedLM',
            'SbertForSequenceClassification',
            'SbertForTokenClassification',
            'SbertModel',
        ],
        'veco': [
            'VecoConfig',
            'VecoForMaskedLM',
            'VecoForSequenceClassification',
            'VecoForTokenClassification',
            'VecoModel',
        ],
        'lstm': [
            'LSTM',
            'LSTMForTokenClassificationWithCRF',
        ],
        'megatron_bert': [
            'MegatronBertConfig',
            'MegatronBertForMaskedLM',
            'MegatronBertModel',
        ],
        'mglm': ['MGLMForTextSummarization'],
        'palm_v2': ['PalmForTextGeneration'],
        'plug_mental': [
            'PlugMentalConfig',
            'PlugMentalModel',
            'PlugMentalForSequenceClassification',
        ],
        'ponet': ['PoNetForMaskedLM', 'PoNetModel', 'PoNetConfig'],
        'space_T_en': ['StarForTextToSql'],
        'space_T_cn': ['TableQuestionAnswering'],
        'space':
        ['SpaceForDialogIntent', 'SpaceForDialogModeling', 'SpaceForDST'],
        'task_models': [
            'ModelForFeatureExtraction',
            'ModelForInformationExtraction',
            'ModelForTextClassification',
            'SingleBackboneTaskModelBase',
            'ModelForTextGeneration',
            'ModelForTextRanking',
            'ModelForTokenClassification',
            'ModelForTokenClassificationWithCRF',
        ],
        'sentence_embedding': ['SentenceEmbedding'],
        'T5': ['T5ForConditionalGeneration'],
        'unite': ['UniTEForTranslationEvaluation'],
        'use': ['UserSatisfactionEstimation'],
        'dgds': [
            'DocumentGroundedDialogGenerateModel',
            'DocumentGroundedDialogRetrievalModel',
            'DocumentGroundedDialogRerankModel'
        ],
        'xlm_roberta': ['XLMRobertaConfig', 'XLMRobertaModel'],
        'llama': [
            'LlamaForTextGeneration', 'LlamaConfig', 'LlamaModel',
            'LlamaTokenizer', 'LlamaTokenizerFast'
        ],
    }

    import sys

    sys.modules[__name__] = LazyImportModule(
        __name__,
        globals()['__file__'],
        _import_structure,
        module_spec=__spec__,
        extra_objects={},
    )
