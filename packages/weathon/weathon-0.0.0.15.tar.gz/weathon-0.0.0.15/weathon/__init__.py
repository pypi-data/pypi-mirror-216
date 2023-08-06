__version__ = '0.0.0.15'
__author__ = 'LiZhen'
__email__ = '16621660628@163.com'
__release_datetime__ = '2099-10-13 08:56:12'



import os
from pathlib import Path

DATA_DIR = Path.home().joinpath("data")
WEATHON_DIR = DATA_DIR.joinpath("weathon")
CACHE_DIR = WEATHON_DIR.joinpath(".cache")
os.environ["DATA_DIR"] = str(DATA_DIR)
os.environ["WEATHON_DIR"] = str(WEATHON_DIR)
os.environ["WEATHON_CACHE_DIR"] = str(CACHE_DIR)

#
#
# from typing import TYPE_CHECKING
#
# from weathon.utils.import_utils import LazyImportModule
#
# if TYPE_CHECKING:
#     from .trainers import Hook, Priority
#     from .exporters import Exporter
#     from .exporters import TfModelExporter
#     from .exporters import TorchModelExporter
#     from weathon.utils.hub import snapshot_download
#     from .metrics import AudioNoiseMetric, Metric, task_default_metrics, ImageColorEnhanceMetric, ImageDenoiseMetric, \
#         ImageInstanceSegmentationCOCOMetric, ImagePortraitEnhancementMetric, SequenceClassificationMetric, \
#         TextGenerationMetric, TokenClassificationMetric, VideoSummarizationMetric, MovieSceneSegmentationMetric, \
#         AccuracyMetric, BleuMetric, ImageInpaintingMetric, ReferringVideoObjectSegmentationMetric, \
#         VideoFrameInterpolationMetric, VideoStabilizationMetric, VideoSuperResolutionMetric, PplMetric, \
#         ImageQualityAssessmentDegradationMetric, ImageQualityAssessmentMosMetric, TextRankingMetric, \
#         LossMetric, ImageColorizationMetric, OCRRecognitionMetric
#     from .models import Model, TorchModel
#     from .pipelines import Pipeline, pipeline
#     from .utils.hub import read_config, create_model_if_not_exist
#     from .utils.logger import get_logger
#     from .datasets import MsDataset
#
# else:
#     _import_structure = {
#         'trainers': [
#             'EpochBasedTrainer', 'TrainingArgs', 'Hook', 'Priority',
#             'build_dataset_from_file'
#         ],
#         'exporters': [
#             'Exporter',
#             'TfModelExporter',
#             'TorchModelExporter',
#         ],
#         'hub.api': ['HubApi'],
#         'hub.snapshot_download': ['snapshot_download'],
#         'hub.push_to_hub': ['push_to_hub', 'push_to_hub_async'],
#         'hub.check_model':
#         ['check_model_is_id', 'check_local_model_is_latest'],
#         'metrics': [
#             'AudioNoiseMetric', 'Metric', 'task_default_metrics',
#             'ImageColorEnhanceMetric', 'ImageDenoiseMetric',
#             'ImageInstanceSegmentationCOCOMetric',
#             'ImagePortraitEnhancementMetric', 'SequenceClassificationMetric',
#             'TextGenerationMetric', 'TokenClassificationMetric',
#             'VideoSummarizationMetric', 'MovieSceneSegmentationMetric',
#             'AccuracyMetric', 'BleuMetric', 'ImageInpaintingMetric',
#             'ReferringVideoObjectSegmentationMetric',
#             'VideoFrameInterpolationMetric', 'VideoStabilizationMetric',
#             'VideoSuperResolutionMetric', 'PplMetric',
#             'ImageQualityAssessmentDegradationMetric',
#             'ImageQualityAssessmentMosMetric', 'TextRankingMetric',
#             'LossMetric', 'ImageColorizationMetric', 'OCRRecognitionMetric'
#         ],
#         'models': ['Model', 'TorchModel'],
#         'preprocessors': ['Preprocessor'],
#         'pipelines': ['Pipeline', 'pipeline'],
#         'utils.hub': ['read_config', 'create_model_if_not_exist'],
#         'utils.logger': ['get_logger'],
#         'datasets': ['MsDataset']
#     }
#
#     import sys
#
#     sys.modules[__name__] = LazyImportModule(
#         __name__,
#         globals()['__file__'],
#         _import_structure,
#         module_spec=__spec__,
#         extra_objects={},
#     )
