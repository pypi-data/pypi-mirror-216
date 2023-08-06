from typing import TYPE_CHECKING

from weathon.utils.import_utils import LazyImportModule

if TYPE_CHECKING:
    from .cv import CartoonTranslationExporter, FaceDetectionSCRFDExporter
    from .nlp import CsanmtForTranslationExporter,SbertForSequenceClassificationExporter, SbertForZeroShotClassificationExporter
else:
    _import_structure = {
        'cv': ['CartoonTranslationExporter', 'FaceDetectionSCRFDExporter'],
        'nlp': [
            'CsanmtForTranslationExporter',
            'SbertForSequenceClassificationExporter',
            'SbertForZeroShotClassificationExporter'
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
