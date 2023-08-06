
from .hub_constant import Fields

# Dataset Constant
class CVDatasets(object):
    # ocr
    icdar2015_ocr_detection = "icdar2015_ocr_detection"


class NLPDatasets(object):
    # text classification
    jd_sentiment_text_classification = "jd_sentiment_text_classification"



class Datasets(CVDatasets, NLPDatasets):

    """
    用于注册模块,module_name
    """

    reverse_field_index = {}
    dataset_template = 'task-template'

    @staticmethod
    def find_field_by_dataset(dataset_name):
        if len(Datasets.reverse_field_index) == 0:
            # Lazy init, not thread safe
            field_dict = {
                Fields.cv: [
                    getattr(Datasets, attr) for attr in dir(CVDatasets)
                    if not attr.startswith('__')
                ],
                Fields.nlp: [
                    getattr(Datasets, attr) for attr in dir(NLPDatasets)
                    if not attr.startswith('__')
                ],
                # Fields.audio: [
                #     getattr(Datasets, attr) for attr in dir(AudioDatasets)
                #     if not attr.startswith('__')
                # ],
                # Fields.multi_modal: [
                #     getattr(Datasets, attr) for attr in dir(MultiModalDatasets)
                #     if not attr.startswith('__')
                # ],
                # Fields.science: [
                #     getattr(Datasets, attr) for attr in dir(ScienceDatasets)
                #     if not attr.startswith('__')
                # ],
            }

            for field, datasets in field_dict.items():
                for dataset in datasets:
                    if dataset in Datasets.reverse_field_index:
                        raise ValueError(f'Duplicate dataset: {dataset}')
                    Datasets.reverse_field_index[dataset] = field

        return Datasets.reverse_field_index.get(dataset_name)
