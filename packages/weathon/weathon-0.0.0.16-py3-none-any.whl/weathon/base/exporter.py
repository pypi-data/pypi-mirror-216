import os
from abc import ABC, abstractmethod
from itertools import chain
from typing import Union, Dict, Any, Mapping,Callable

import torch
from torch import nn

from weathon.registry import build_exporter
from weathon.utils.config.config import Config, ConfigDict
from weathon.utils.constants import ModelFile
from weathon.utils.exporter_utils import replace_call
from weathon.utils.logger import get_logger
from weathon.utils.test_utils.regress_test_utils import numpify_tensor_nested
from weathon.utils.test_utils.test_utils import compare_arguments_nested
from torch.onnx import export as onnx_export
from .model import BaseModel
from .modeloutput import BaseModelOutput
from .pipeline import collate_fn

logger = get_logger(__name__)




class BaseExporter(ABC):
    """Exporter base class to output model to onnx, torch_script, graphdef, etc.
    """

    def __init__(self, model=None):
        self.model = model

    @classmethod
    def from_model(cls, model: Union[BaseModel, str], **kwargs):
        """Build the Exporter instance.

        Args:
            model: A Model instance or a model id or a model dir, the configuration.json file besides to which
            will be used to create the exporter instance.
            kwargs: Extra kwargs used to create the Exporter instance.

        Returns:
            The Exporter instance
        """
        if isinstance(model, str):
            model = BaseModel.from_pretrained(model)

        assert hasattr(model, 'model_dir')
        model_dir = model.model_dir
        cfg = Config.from_file(os.path.join(model_dir, ModelFile.CONFIGURATION))
        task_name = cfg.task
        if hasattr(model, 'group_key'):
            task_name = model.group_key
        model_cfg = cfg.model
        if hasattr(model_cfg, 'model_type') and not hasattr(model_cfg, 'type'):
            model_cfg.type = model_cfg.model_type
        export_cfg = ConfigDict({'type': model_cfg.type})
        if hasattr(cfg, 'export'):
            export_cfg.update(cfg.export)
        export_cfg['model'] = model
        try:
            exporter = build_exporter(export_cfg, task_name, kwargs)
        except KeyError as e:
            raise KeyError(
                f'The exporting of model \'{model_cfg.type}\' with task: \'{task_name}\' '
                f'is not supported currently.') from e
        return exporter

    @abstractmethod
    def export_onnx(self, output_dir: str, opset=13, **kwargs):
        """Export the model as onnx format files.

        In some cases,  several files may be generated,
        So please return a dict which contains the generated name with the file path.

        Args:
            opset: The version of the ONNX operator set to use.
            output_dir: The output dir.
            kwargs: In this default implementation,
                kwargs will be carried to generate_dummy_inputs as extra arguments (like input shape).

        Returns:
            A dict contains the model name with the model file path.
        """
        pass


class TorchModelExporter(BaseExporter):
    """The torch base class of exporter.

    This class provides the default implementations for exporting onnx and torch script.
    Each specific model may implement its own exporter by overriding the export_onnx/export_torch_script,
    and to provide implementations for generate_dummy_inputs/inputs/outputs methods.
    """

    def export_onnx(self, output_dir: str, opset=13, **kwargs):
        """Export the model as onnx format files.

        In some cases,  several files may be generated,
        So please return a dict which contains the generated name with the file path.

        Args:
            opset: The version of the ONNX operator set to use.
            output_dir: The output dir.
            kwargs:
                model: A model instance which will replace the exporting of self.model.
                In this default implementation,
                you can pass the arguments needed by _torch_export_onnx, other unrecognized args
                will be carried to generate_dummy_inputs as extra arguments (such as input shape).

        Returns:
            A dict containing the model key - model file path pairs.
        """
        model = self.model if 'model' not in kwargs else kwargs.pop('model')
        if not isinstance(model, nn.Module) and hasattr(model, 'model'):
            model = model.model
        onnx_file = os.path.join(output_dir, ModelFile.ONNX_MODEL_FILE)
        self._torch_export_onnx(model, onnx_file, opset=opset, **kwargs)
        return {'model': onnx_file}

    def export_torch_script(self, output_dir: str, **kwargs):
        """Export the model as torch script files.

        In some cases,  several files may be generated,
        So please return a dict which contains the generated name with the file path.

        Args:
            output_dir: The output dir.
            kwargs:
            model: A model instance which will replace the exporting of self.model.
            In this default implementation,
            you can pass the arguments needed by _torch_export_torch_script, other unrecognized args
            will be carried to generate_dummy_inputs as extra arguments (like input shape).

        Returns:
            A dict contains the model name with the model file path.
        """
        model = self.model if 'model' not in kwargs else kwargs.pop('model')
        if not isinstance(model, nn.Module) and hasattr(model, 'model'):
            model = model.model
        ts_file = os.path.join(output_dir, ModelFile.TS_MODEL_FILE)
        # generate ts by tracing
        self._torch_export_torch_script(model, ts_file, **kwargs)
        return {'model': ts_file}

    def generate_dummy_inputs(self, **kwargs) -> Dict[str, Any]:
        """Generate dummy inputs for model exportation to onnx or other formats by tracing.

        Returns:
            Dummy inputs.
        """
        return None

    @property
    def inputs(self) -> Mapping[str, Mapping[int, str]]:
        """Return an ordered dict contains the model's input arguments name with their dynamic axis.

        About the information of dynamic axis please check the dynamic_axes argument of torch.onnx.export function
        """
        return None

    @property
    def outputs(self) -> Mapping[str, Mapping[int, str]]:
        """Return an ordered dict contains the model's output arguments name with their dynamic axis.

        About the information of dynamic axis please check the dynamic_axes argument of torch.onnx.export function
        """
        return None

    @staticmethod
    def _decide_input_format(model, args):
        import inspect

        def _signature(model) -> inspect.Signature:
            should_be_callable = getattr(model, 'forward', model)
            if callable(should_be_callable):
                return inspect.signature(should_be_callable)
            raise ValueError('model has no forward method and is not callable')

        try:
            sig = _signature(model)
        except ValueError as e:
            logger.warning('%s, skipping _decide_input_format' % e)
            return args
        try:
            ordered_list_keys = list(sig.parameters.keys())
            if ordered_list_keys[0] == 'self':
                ordered_list_keys = ordered_list_keys[1:]
            args_dict: Dict = {}
            if isinstance(args, list):
                args_list = args
            elif isinstance(args, tuple):
                args_list = list(args)
            else:
                args_list = [args]
            if isinstance(args_list[-1], Mapping):
                args_dict = args_list[-1]
                args_list = args_list[:-1]
            n_nonkeyword = len(args_list)
            for optional_arg in ordered_list_keys[n_nonkeyword:]:
                if optional_arg in args_dict:
                    args_list.append(args_dict[optional_arg])
                # Check if this arg has a default value
                else:
                    param = sig.parameters[optional_arg]
                    if param.default != param.empty:
                        args_list.append(param.default)
            args = args_list if isinstance(args, list) else tuple(args_list)
        # Cases of models with no input args
        except IndexError:
            logger.warning('No input args, skipping _decide_input_format')
        except Exception as e:
            logger.warning('Skipping _decide_input_format\n {}'.format(
                e.args[0]))

        return args

    def _torch_export_onnx(self,
                           model: nn.Module,
                           output: str,
                           opset: int = 13,
                           device: str = 'cpu',
                           validation: bool = True,
                           rtol: float = None,
                           atol: float = None,
                           **kwargs):
        """Export the model to an onnx format file.

        Args:
            model: A torch.nn.Module instance to export.
            output: The output file.
            opset: The version of the ONNX operator set to use.
            device: The device used to forward.
            validation: Whether validate the export file.
            rtol: The rtol used to regress the outputs.
            atol: The atol used to regress the outputs.
            kwargs:
                dummy_inputs: A dummy inputs which will replace the calling of self.generate_dummy_inputs().
                inputs: An inputs structure which will replace the calling of self.inputs.
                outputs: An outputs structure which will replace the calling of self.outputs.
        """

        dummy_inputs = self.generate_dummy_inputs(**kwargs) if 'dummy_inputs' not in kwargs else kwargs.pop('dummy_inputs')
        inputs = self.inputs if 'inputs' not in kwargs else kwargs.pop('inputs')
        outputs = self.outputs if 'outputs' not in kwargs else kwargs.pop('outputs')
        if dummy_inputs is None or inputs is None or outputs is None:
            raise NotImplementedError('Model property dummy_inputs,inputs,outputs must be set.')

        with torch.no_grad():
            model.eval()
            device = torch.device(device)
            model.to(device)
            dummy_inputs = collate_fn(dummy_inputs, device)

            if isinstance(dummy_inputs, Mapping):
                dummy_inputs = dict(dummy_inputs)
            onnx_outputs = list(outputs.keys())

            with replace_call():
                onnx_export(model, (dummy_inputs,), f=output,
                            input_names=list(inputs.keys()),
                            output_names=onnx_outputs,
                            dynamic_axes={
                                name: axes
                                for name, axes in chain(inputs.items(),
                                                        outputs.items())
                            },
                            do_constant_folding=True,
                            opset_version=opset,
                            )

        if validation:
            self._validate_onnx_model(dummy_inputs, model, output,
                                      onnx_outputs, rtol, atol)

    def _validate_onnx_model(self,
                             dummy_inputs,
                             model,
                             output,
                             onnx_outputs,
                             rtol: float = None,
                             atol: float = None):
        try:
            import onnx
            import onnxruntime as ort
        except ImportError:
            logger.warning('Cannot validate the exported onnx file, because the installation of onnx or onnxruntime cannot be found')
            return
        onnx_model = onnx.load(output)
        onnx.checker.check_model(onnx_model)
        ort_session = ort.InferenceSession(output)
        with torch.no_grad():
            model.eval()
            outputs_origin = model.forward(*self._decide_input_format(model, dummy_inputs))
        if isinstance(outputs_origin, (Mapping, BaseModelOutput)):
            outputs_origin = list(numpify_tensor_nested(outputs_origin).values())
        elif isinstance(outputs_origin, (tuple, list)):
            outputs_origin = list(numpify_tensor_nested(outputs_origin))

        outputs = ort_session.run(
            onnx_outputs,
            numpify_tensor_nested(dummy_inputs),
        )
        outputs = numpify_tensor_nested(outputs)
        if isinstance(outputs, dict):
            outputs = list(outputs.values())
        elif isinstance(outputs, tuple):
            outputs = list(outputs)

        tols = {}
        if rtol is not None:
            tols['rtol'] = rtol
        if atol is not None:
            tols['atol'] = atol
        print(outputs)
        print(outputs_origin)
        if not compare_arguments_nested('Onnx model output match failed',
                                        outputs, outputs_origin, **tols):
            raise RuntimeError(
                'export onnx failed because of validation error.')

    def _torch_export_torch_script(self,
                                   model: nn.Module,
                                   output: str,
                                   device: str = 'cpu',
                                   validation: bool = True,
                                   rtol: float = None,
                                   atol: float = None,
                                   strict: bool = True,
                                   **kwargs):
        """Export the model to a torch script file.

        Args:
            model: A torch.nn.Module instance to export.
            output: The output file.
            device: The device used to forward.
            validation: Whether validate the export file.
            rtol: The rtol used to regress the outputs.
            atol: The atol used to regress the outputs.
            strict: strict mode in torch script tracing.
            kwargs:
                dummy_inputs: A dummy inputs which will replace the calling of self.generate_dummy_inputs().
        """

        model.eval()
        dummy_param = 'dummy_inputs' not in kwargs
        dummy_inputs = self.generate_dummy_inputs(
            **kwargs) if dummy_param else kwargs.pop('dummy_inputs')
        if dummy_inputs is None:
            raise NotImplementedError('Model property dummy_inputs must be set.')
        dummy_inputs = collate_fn(dummy_inputs, device)
        if isinstance(dummy_inputs, Mapping):
            dummy_inputs_filter = []
            for _input in self._decide_input_format(model, dummy_inputs):
                if _input is not None:
                    dummy_inputs_filter.append(_input)
                else:
                    break

            if len(dummy_inputs) != len(dummy_inputs_filter):
                logger.warning(
                    f'Dummy inputs is not continuous in the forward method, '
                    f'origin length: {len(dummy_inputs)}, '
                    f'the length after filtering: {len(dummy_inputs_filter)}')
            dummy_inputs = dummy_inputs_filter

        with torch.no_grad():
            model.eval()
            with replace_call():
                traced_model = torch.jit.trace(
                    model, tuple(dummy_inputs), strict=strict)
        torch.jit.save(traced_model, output)

        if validation:
            self._validate_torch_script_model(dummy_inputs, model, output,
                                              rtol, atol)

    def _validate_torch_script_model(self, dummy_inputs, model, output, rtol,
                                     atol):
        ts_model = torch.jit.load(output)
        with torch.no_grad():
            model.eval()
            ts_model.eval()
            outputs = ts_model.forward(*dummy_inputs)
            outputs = numpify_tensor_nested(outputs)
            outputs_origin = model.forward(*dummy_inputs)
            outputs_origin = numpify_tensor_nested(outputs_origin)
            if isinstance(outputs, dict):
                outputs = list(outputs.values())
            if isinstance(outputs_origin, dict):
                outputs_origin = list(outputs_origin.values())
        tols = {}
        if rtol is not None:
            tols['rtol'] = rtol
        if atol is not None:
            tols['atol'] = atol
        if not compare_arguments_nested(
                'Torch script model output match failed', outputs,
                outputs_origin, **tols):
            raise RuntimeError(
                'export torch script failed because of validation error.')


class TfModelExporter(BaseExporter):

    def generate_dummy_inputs(self, **kwargs) -> Dict[str, Any]:
        """Generate dummy inputs for model exportation to onnx or other formats by tracing.

        Returns:
            Dummy inputs that matches the specific model input, the matched preprocessor can be used here.
        """
        return None

    def export_onnx(self, output_dir: str, opset=13, **kwargs):
        model = self.model if 'model' not in kwargs else kwargs.pop('model')
        onnx_file = os.path.join(output_dir, ModelFile.ONNX_MODEL_FILE)
        self._tf2_export_onnx(model, onnx_file, opset=opset, **kwargs)
        return {'model': onnx_file}

    def export_saved_model(self, output_dir: str, **kwargs):
        raise NotImplementedError()

    def export_frozen_graph_def(self, output_dir: str, **kwargs):
        raise NotImplementedError()

    def _tf2_export_onnx(self,
                         model,
                         output: str,
                         opset: int = 13,
                         validation: bool = True,
                         rtol: float = None,
                         atol: float = None,
                         call_func: Callable = None,
                         **kwargs):
        logger.info(
            'Important: This exporting function only supports models of tf2.0 or above.'
        )
        import onnx
        import tf2onnx
        dummy_inputs = self.generate_dummy_inputs(
            **kwargs) if 'dummy_inputs' not in kwargs else kwargs.pop(
            'dummy_inputs')
        if dummy_inputs is None:
            raise NotImplementedError('Model property dummy_inputs,inputs,outputs must be set.')

        input_signature = [
            tf.TensorSpec.from_tensor(tensor, name=key)
            for key, tensor in dummy_inputs.items()
        ]
        onnx_model, _ = tf2onnx.convert.from_keras(
            model, input_signature, opset=opset)
        onnx.save(onnx_model, output)

        if validation:
            self._validate_model(dummy_inputs, model, output, rtol, atol,
                                 call_func)

    def _validate_model(
            self,
            dummy_inputs,
            model,
            output,
            rtol: float = None,
            atol: float = None,
            call_func: Callable = None,
    ):
        try:
            import onnx
            import onnxruntime as ort
        except ImportError:
            logger.warn(
                'Cannot validate the exported onnx file, because '
                'the installation of onnx or onnxruntime cannot be found')
            return

        def tensor_nested_numpify(tensors):
            if isinstance(tensors, (list, tuple)):
                return type(tensors)(tensor_nested_numpify(t) for t in tensors)
            if isinstance(tensors, Mapping):
                # return dict
                return {
                    k: tensor_nested_numpify(t)
                    for k, t in tensors.items()
                }
            if isinstance(tensors, tf.Tensor):
                t = tensors.cpu()
                return t.numpy()
            return tensors

        onnx_model = onnx.load(output)
        onnx.checker.check_model(onnx_model, full_check=True)
        ort_session = ort.InferenceSession(output)
        outputs_origin = call_func(
            dummy_inputs) if call_func is not None else model(dummy_inputs)
        if isinstance(outputs_origin, (Mapping, BaseModelOutput)):
            outputs_origin = list(
                tensor_nested_numpify(outputs_origin).values())
        elif isinstance(outputs_origin, (tuple, list)):
            outputs_origin = list(tensor_nested_numpify(outputs_origin))
        outputs = ort_session.run(
            None,
            tensor_nested_numpify(dummy_inputs),
        )
        outputs = tensor_nested_numpify(outputs)
        if isinstance(outputs, dict):
            outputs = list(outputs.values())
        elif isinstance(outputs, tuple):
            outputs = list(outputs)

        tols = {}
        if rtol is not None:
            tols['rtol'] = rtol
        if atol is not None:
            tols['atol'] = atol
        if not compare_arguments_nested('Onnx model output match failed',outputs, outputs_origin, **tols):
            raise RuntimeError('export onnx failed because of validation error.')
