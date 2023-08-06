from typing import Any, Dict, Optional, Union

import torch

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.multi_modal import (CLIP_Interrogator, MPlugForAllTasks,
                                           OfaForAllTasks)
from weathon.pipelines.base import Model, Pipeline
from weathon.registry import PIPELINES
from weathon.pipelines.util import batch_process
from weathon.preprocessors import (
    ImageCaptioningClipInterrogatorPreprocessor, MPlugPreprocessor,
    OfaPreprocessor, Preprocessor)
from weathon.utils.constants import ModelFile, Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.image_captioning, module_name=Pipelines.image_captioning)
class ImageCaptioningPipeline(Pipeline):

    def __init__(self,
                 model: Union[Model, str],
                 preprocessor: Optional[Preprocessor] = None,
                 **kwargs):
        """
        use `model` and `preprocessor` to create a image captioning pipeline for prediction
        Args:
            model: model id on modelscope hub.
        Examples:
        from weathon.pipelines import pipeline
        from weathon.utils.constants import Tasks

        model_id = 'damo/cv_clip-interrogator'
        input_image = "test.png"

        pipeline_ci = pipeline(Tasks.image_captioning, model=model_id)
        print(pipeline_ci(input_image))


        """
        super().__init__(model=model, preprocessor=preprocessor, **kwargs)
        self.model.eval()
        assert isinstance(self.model, Model), \
            f'please check whether model config exists in {ModelFile.CONFIGURATION}'
        if preprocessor is None:

            if isinstance(self.model, OfaForAllTasks):
                self.preprocessor = OfaPreprocessor(self.model.model_dir)
            elif isinstance(self.model, MPlugForAllTasks):
                self.preprocessor = MPlugPreprocessor(self.model.model_dir)
            elif isinstance(self.model, CLIP_Interrogator):
                self.preprocessor = ImageCaptioningClipInterrogatorPreprocessor(
                )

    def _batch(self, data):
        if isinstance(self.model, OfaForAllTasks):
            return batch_process(self.model, data)
        elif isinstance(self.model, MPlugForAllTasks):
            from transformers.tokenization_utils_base import BatchEncoding
            batch_data = dict(train=data[0]['train'])
            batch_data['image'] = torch.cat([d['image'] for d in data])
            question = {}
            for k in data[0]['question'].keys():
                question[k] = torch.cat([d['question'][k] for d in data])
            batch_data['question'] = BatchEncoding(question)
            return batch_data
        else:
            return super(ImageCaptioningPipeline, self)._batch(data)

    def forward(self, inputs: Dict[str, Any],
                **forward_params) -> Dict[str, Any]:
        with torch.no_grad():
            return super().forward(inputs, **forward_params)

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return inputs
