from typing import Any, Dict, Optional, Union

from weathon.utils.constants.metainfo import Pipelines
from weathon.models.multi_modal.vldoc.model import VLDocForDocVLEmbedding
from weathon.pipelines.base import Model, Pipeline
from weathon.registry import PIPELINES
from weathon.preprocessors.multi_modal import (Preprocessor,
                                                  VLDocPreprocessor)
from weathon.utils.constants import Tasks
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.document_vl_embedding, module_name=Pipelines.document_vl_embedding)
class DocumentVLEmbeddingPipeline(Pipeline):

    def __init__(self,
                 model: Union[Model, str],
                 preprocessor: Optional[Preprocessor] = None,
                 **kwargs):
        """ The pipeline for multi-modal document embedding generation.

        Args:
            model: model id on modelscope hub.
            preprocessor: type `Preprocessor`. If None, `VLDocPreprocessor` is used.

        Examples:

        >>> from weathon.models import Model
        >>> from weathon.pipelines import pipeline
        >>> model = Model.from_pretrained(
            'damo/multi-modal_convnext-roberta-base_vldoc-embedding')
        >>> doc_VL_emb_pipeline = pipeline(task='document-vl-embedding', model=model)
        >>> inp = {
                'images': ['data/demo.png'],
                'ocr_info_paths': ['data/demo.json']
            }
        >>> result = doc_VL_emb_pipeline(inp)
        """

        super().__init__(model=model, preprocessor=preprocessor, **kwargs)
        self.model.eval()
        if preprocessor is None:
            if isinstance(self.model, VLDocForDocVLEmbedding):
                self.preprocessor = VLDocPreprocessor(self.model.model_dir)
            else:
                raise NotImplementedError

    def forward(self, encodings: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in encodings.items():
            encodings[k] = encodings[k].to(self.device)
        return self.model(**encodings)

    def postprocess(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return inputs
