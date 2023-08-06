
import os
import os.path as osp
from typing import List, Optional, Union


from weathon.utils.constants import DEFAULT_MODEL_REVISION, ModelFile, Invoke
from weathon.utils.constants.metainfo import DEFAULT_MODEL_FOR_PIPELINE
from weathon.utils.constants.pipeline_inputs import INPUT_TYPE, InputType
from weathon.utils.hub.api import HubApi
from weathon.utils.config.config import Config
from weathon.utils.hub.utils import snapshot_download, model_file_download
from weathon.utils.logger import get_logger

logger = get_logger()

def check_input_type(input_type, input):
    expected_type = INPUT_TYPE[input_type]
    if input_type == InputType.VIDEO:
        # special type checking using class name, to avoid introduction of opencv dependency into fundamental framework.
        assert type(input).__name__ == 'VideoCapture' or isinstance(input, expected_type),\
            f'invalid input type for {input_type}, expected {expected_type} but got {type(input)}\n {input}'
    else:
        assert isinstance(input, expected_type), \
            f'invalid input type for {input_type}, expected {expected_type} but got {type(input)}\n {input}'





def is_config_has_model(cfg_file):
    try:
        cfg = Config.from_file(cfg_file)
        return hasattr(cfg, 'model')
    except Exception as e:
        logger.error(f'parse config file {cfg_file} failed: {e}')
        return False


def is_official_hub_path(path: Union[str, List],
                         revision: Optional[str] = DEFAULT_MODEL_REVISION):
    """ Whether path is an official hub name or a valid local
    path to official hub directory.
    """

    def is_official_hub_impl(path):
        if osp.exists(path):
            cfg_file = osp.join(path, ModelFile.CONFIGURATION)
            return osp.exists(cfg_file)
        else:
            try:
                _ = HubApi().get_model(path, revision=revision)
                return True
            except Exception as e:
                raise ValueError(f'invalid model repo path {e}')

    if isinstance(path, str):
        return is_official_hub_impl(path)
    else:
        results = [is_official_hub_impl(m) for m in path]
        all_true = all(results)
        any_true = any(results)
        if any_true and not all_true:
            raise ValueError(
                f'some model are hub address, some are not, model list: {path}'
            )

        return all_true


def is_model(path: Union[str, List]):
    """ whether path is a valid modelhub path and containing model config
    """

    def is_modelhub_path_impl(path):
        if osp.exists(path):
            cfg_file = osp.join(path, ModelFile.CONFIGURATION)
            if osp.exists(cfg_file):
                return is_config_has_model(cfg_file)
            else:
                return False
        else:
            try:
                cfg_file = model_file_download(path, ModelFile.CONFIGURATION)
                return is_config_has_model(cfg_file)
            except Exception:
                return False

    if isinstance(path, str):
        return is_modelhub_path_impl(path)
    else:
        results = [is_modelhub_path_impl(m) for m in path]
        all_true = all(results)
        any_true = any(results)
        if any_true and not all_true:
            raise ValueError(
                f'some models are hub address, some are not, model list: {path}'
            )

        return all_true


def batch_process(model, data):
    import torch
    if model.__class__.__name__ == 'OfaForAllTasks':
        # collate batch data due to the nested data structure
        assert isinstance(data, list)
        batch_data = {
            'nsentences': len(data),
            'samples': [d['samples'][0] for d in data],
            'net_input': {}
        }
        for k in data[0]['net_input'].keys():
            batch_data['net_input'][k] = torch.cat(
                [d['net_input'][k] for d in data])
        if 'w_resize_ratios' in data[0]:
            batch_data['w_resize_ratios'] = torch.cat(
                [d['w_resize_ratios'] for d in data])
        if 'h_resize_ratios' in data[0]:
            batch_data['h_resize_ratios'] = torch.cat(
                [d['h_resize_ratios'] for d in data])

        return batch_data



def normalize_model_input(model, model_revision):
    """ normalize the input model, to ensure that a model str is a valid local path: in other words,
    for model represented by a model id, the model shall be downloaded locally
    """
    if isinstance(model, str) and is_official_hub_path(model, model_revision):
        # skip revision download if model is a local directory
        if not os.path.exists(model):
            # note that if there is already a local copy, snapshot_download will check and skip downloading
            model = snapshot_download(
                model,
                revision=model_revision,
                user_agent={Invoke.KEY: Invoke.PIPELINE})
    elif isinstance(model, list) and isinstance(model[0], str):
        for idx in range(len(model)):
            if is_official_hub_path(
                    model[idx],
                    model_revision) and not os.path.exists(model[idx]):
                model[idx] = snapshot_download(
                    model[idx],
                    revision=model_revision,
                    user_agent={Invoke.KEY: Invoke.PIPELINE})
    return model


def add_default_pipeline_info(task: str,
                              model_name: str,
                              modelhub_name: str = None,
                              overwrite: bool = False):
    """ Add default model for a task.

    Args:
        task (str): task name.
        model_name (str): model_name.
        modelhub_name (str): name for default modelhub.
        overwrite (bool): overwrite default info.
    """
    if not overwrite:
        assert task not in DEFAULT_MODEL_FOR_PIPELINE, \
            f'task {task} already has default model.'

    DEFAULT_MODEL_FOR_PIPELINE[task] = (model_name, modelhub_name)


def get_default_pipeline_info(task):
    """ Get default info for certain task.

    Args:
        task (str): task name.

    Return:
        A tuple: first element is pipeline name(model_name), second element
            is modelhub name.
    """
    from weathon.registry import PIPELINES
    if task not in DEFAULT_MODEL_FOR_PIPELINE:
        # support pipeline which does not register default model
        pipeline_name = list(PIPELINES.modules[task].keys())[0]
        default_model = None
    else:
        pipeline_name, default_model = DEFAULT_MODEL_FOR_PIPELINE[task]
    return pipeline_name, default_model
