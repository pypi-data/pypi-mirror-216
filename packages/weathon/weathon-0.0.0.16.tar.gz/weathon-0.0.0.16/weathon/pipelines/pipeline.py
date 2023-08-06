import os
from typing import List, Optional, Union

from weathon.utils.hub import snapshot_download
from weathon.utils.constants.metainfo import DEFAULT_MODEL_FOR_PIPELINE
from weathon.base import BaseModel
from weathon.utils.config.config import ConfigDict, check_config
from weathon.utils.constant import DEFAULT_MODEL_REVISION, Invoke
from weathon.utils.hub.utils import read_config
from weathon.utils.plugins import (register_modelhub_repo, register_plugins_repo)
from weathon.utils.registry import Registry, build_from_cfg
from weathon.base import BasePipeline
from .util import is_official_hub_path

def pipeline(task: str = None,
             model: Union[str, List[str], Model, List[Model]] = None,
             preprocessor=None,
             config_file: str = None,
             pipeline_name: str = None,
             framework: str = None,
             device: str = 'gpu',
             model_revision: Optional[str] = DEFAULT_MODEL_REVISION,
             **kwargs) -> Pipeline:
    """ Factory method to build an obj:`Pipeline`.


    Args:
        task (str): Task name defining which pipeline will be returned.
        model (str or List[str] or obj:`Model` or obj:list[`Model`]): (list of) model name or model object.
        preprocessor: preprocessor object.
        config_file (str, optional): path to config file.
        pipeline_name (str, optional): pipeline class name or alias name.
        framework (str, optional): framework type.
        model_revision: revision of model(s) if getting from model hub, for multiple models, expecting
        all models to have the same revision
        device (str, optional): whether to use gpu or cpu is used to do inference.

    Return:
        pipeline (obj:`Pipeline`): pipeline object for certain task.

    Examples:
        >>> # Using default model for a task
        >>> p = pipeline('image-classification')
        >>> # Using pipeline with a model name
        >>> p = pipeline('text-classification', model='damo/distilbert-base-uncased')
        >>> # Using pipeline with a model object
        >>> resnet = Model.from_pretrained('Resnet')
        >>> p = pipeline('image-classification', model=resnet)
        >>> # Using pipeline with a list of model names
        >>> p = pipeline('audio-kws', model=['damo/audio-tts', 'damo/auto-tts2'])
    """
    if task is None and pipeline_name is None:
        raise ValueError('task or pipeline_name is required')

    model = normalize_model_input(model, model_revision)
    pipeline_props = {'type': pipeline_name}
    if pipeline_name is None:
        # get default pipeline for this task
        if isinstance(model, str) \
           or (isinstance(model, list) and isinstance(model[0], str)):
            if is_official_hub_path(model, revision=model_revision):
                # read config file from hub and parse
                cfg = read_config(
                    model, revision=model_revision) if isinstance(
                        model, str) else read_config(
                            model[0], revision=model_revision)
                check_config(cfg)
                register_plugins_repo(cfg.safe_get('plugins'))
                register_modelhub_repo(model, cfg.get('allow_remote', False))
                pipeline_props = cfg.pipeline
        elif model is not None:
            # get pipeline info from Model object
            first_model = model[0] if isinstance(model, list) else model
            if not hasattr(first_model, 'pipeline'):
                # model is instantiated by user, we should parse config again
                cfg = read_config(first_model.model_dir)
                check_config(cfg)
                first_model.pipeline = cfg.pipeline
            pipeline_props = first_model.pipeline
        else:
            pipeline_name, default_model_repo = get_default_pipeline_info(task)
            model = normalize_model_input(default_model_repo, model_revision)
            pipeline_props = {'type': pipeline_name}

    pipeline_props['model'] = model
    pipeline_props['device'] = device
    cfg = ConfigDict(pipeline_props)

    if kwargs:
        cfg.update(kwargs)

    if preprocessor is not None:
        cfg.preprocessor = preprocessor

    return build_pipeline(cfg, task_name=task)


