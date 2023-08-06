from weathon.utils.constants.metainfo import Heads, TaskModels
from weathon.registry import MODELS
from weathon.models.nlp.task_models.task_model import EncoderModel
from weathon.utils.constants import Tasks, Datasets

__all__ = ['ModelForTextClassification']

from weathon.utils.hub.utils import parse_label_mapping


@MODELS.register_module(Tasks.text_classification, module_name=Datasets.jd_sentiment_text_classification)
@MODELS.register_module(Tasks.text_classification, module_name=TaskModels.text_classification)
class ModelForTextClassification(EncoderModel):
    task = Tasks.text_classification

    # The default base head type is text-classification for this head
    head_type = Heads.text_classification

    def __init__(self, model_dir: str, *args, **kwargs):
        """initialize the sequence classification model from the `model_dir` path.

        Args:
            model_dir (str): the model path.
        """
        # get the num_labels from label_mapping.json
        self.id2label = {}

        # get the num_labels
        num_labels = kwargs.get('num_labels')
        if num_labels is None:
            label2id = parse_label_mapping(model_dir)
            if label2id is not None and len(label2id) > 0:
                num_labels = len(label2id)
            self.id2label = {id: label for label, id in label2id.items()}
        kwargs['num_labels'] = num_labels
        super().__init__(model_dir, *args, **kwargs)

    def parse_head_cfg(self):
        head_cfg = super().parse_head_cfg()
        if hasattr(head_cfg, 'classifier_dropout'):
            head_cfg['classifier_dropout'] = (
                head_cfg.classifier_dropout if head_cfg['classifier_dropout']
                is not None else head_cfg.hidden_dropout_prob)
        else:
            head_cfg['classifier_dropout'] = head_cfg.hidden_dropout_prob
        head_cfg['num_labels'] = self.config.num_labels
        return head_cfg
