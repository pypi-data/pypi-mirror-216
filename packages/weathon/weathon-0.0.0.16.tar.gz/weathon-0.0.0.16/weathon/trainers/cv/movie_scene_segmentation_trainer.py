from weathon.base import EpochBasedTrainer
from weathon.registry import TRAINERS
from weathon.utils.constants.metainfo import Trainers


@TRAINERS.register_module(module_name=Trainers.movie_scene_segmentation)
class MovieSceneSegmentationTrainer(EpochBasedTrainer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def train(self, *args, **kwargs):
        super().train(*args, **kwargs)

    def evaluate(self, *args, **kwargs):
        metric_values = super().evaluate(*args, **kwargs)
        return metric_values

    def prediction_step(self, model, inputs):
        pass
