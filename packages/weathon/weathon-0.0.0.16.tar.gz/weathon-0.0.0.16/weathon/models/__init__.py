from weathon.utils.import_utils import is_torch_available
from . import audio, cv, multi_modal, nlp

if is_torch_available():
    from weathon.base import TorchModel, TorchHead
