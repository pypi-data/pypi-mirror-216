from weathon.base import BasePipeline
from weathon.utils.constants.metainfo import Pipelines
from weathon.models.cv.ocr_recognition import OCRRecognition
from weathon.registry import PIPELINES
from weathon.utils.constants import Tasks
from weathon.utils.constants.output_constant import OutputKeys
from weathon.utils.logger import get_logger

logger = get_logger()


@PIPELINES.register_module(
    Tasks.ocr_recognition, module_name=Pipelines.ocr_recognition)
class OCRRecognitionPipeline(BasePipeline):
    """ OCR Recognition Pipeline.

    Example:

    ```python
    >>> from weathon.pipelines import pipeline

    >>> ocr_recognition = pipeline('ocr-recognition', 'damo/cv_crnn_ocr-recognition-general_damo')
    >>> ocr_recognition("http://duguang-labelling.oss-cn-shanghai.aliyuncs.com"
        "/mass_img_tmp_20220922/ocr_recognition_handwritten.jpg")

        {'text': '电子元器件提供BOM配单'}
    ```
    """

    def __init__(self, model: str, **kwargs):
        """
        use `model` to create a ocr recognition pipeline for prediction
        Args:
            model: model id on modelscope hub or `OCRRecognition` Model.
            preprocessor: `OCRRecognitionPreprocessor`.
        """
        assert isinstance(model, str), 'model must be a single str'
        super().__init__(model=model, **kwargs)
        logger.info(f'loading model from dir {model}')
        self.ocr_recognizer = self.model.to(self.device)
        self.ocr_recognizer.eval()
        logger.info('loading model done')

    def __call__(self, input, **kwargs):
        """
        Recognize text sequence in the text image.

        Args:
            input (`Image`):
                The pipeline handles three types of images:

                - A string containing an HTTP link pointing to an image
                - A string containing a local path to an image
                - An image loaded in PIL or opencv directly

                The pipeline currently supports single image input.

        Return:
            A text sequence (string) of the input text image.
        """
        return super().__call__(input, **kwargs)

    def preprocess(self, inputs):
        outputs = self.preprocessor(inputs)
        return outputs

    def forward(self, inputs):
        outputs = self.ocr_recognizer(inputs)
        return outputs

    def postprocess(self, inputs):
        outputs = {OutputKeys.TEXT: inputs['preds']}
        return outputs
