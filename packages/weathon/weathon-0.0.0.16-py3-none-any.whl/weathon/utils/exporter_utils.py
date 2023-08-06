from contextlib import contextmanager

from weathon.base.model import TorchModel


@contextmanager
def replace_call():
    """This function is used to recover the original call method.

    The Model class of modelscope overrides the call method. When exporting to onnx or torchscript, torch will
    prepare the parameters as the prototype of forward method, and trace the call method, this causes
    problems. Here we recover the call method to the default implementation of torch.nn.Module, and change it
    back after the tracing was done.
    """
    TorchModel.call_origin, TorchModel.__call__ = TorchModel.__call__, TorchModel._call_impl
    yield
    TorchModel.__call__ = TorchModel.call_origin
    del TorchModel.call_origin