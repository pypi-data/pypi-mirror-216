from weathon.registry.registry import Registry,build_from_cfg
from weathon.utils.config.config import ConfigDict
from weathon.utils.constants import DEFAULT_MODEL_REVISION
from weathon.utils.constants.metainfo import Trainers
from weathon.utils.hub.utils import read_config
from weathon.utils.pipeline_utils import is_official_hub_path, normalize_model_input
from weathon.utils.plugins import register_plugins_repo, register_modelhub_repo

TRAINERS = Registry('trainers')


def build_trainer(cfg:ConfigDict,task_name:str=None, default_args: dict = None):
    """ build trainer given a trainer name

    Args:
        name (str, optional):  Trainer name, if None, default trainer
            will be used.
        default_args (dict, optional): Default initialization arguments.
    """
    # TODO: 设置默认参数值
    cfg["type"] = default_args.get("type", cfg.get("type", Trainers.default))
    cfg = cfg.to_dict()
    model = default_args.get('model', None)
    model_revision = default_args.get('model_revision', DEFAULT_MODEL_REVISION)

    if isinstance(model, str) or (isinstance(model, list) and isinstance(model[0], str)):
        if is_official_hub_path(model, revision=model_revision):
            # read config file from hub and parse
            configuration = read_config(model, revision=model_revision) if isinstance(model, str) else read_config(model[0], revision=model_revision)
            model_dir = normalize_model_input(model, model_revision)
            register_plugins_repo(configuration.safe_get('plugins'))
            register_modelhub_repo(model_dir, configuration.get('allow_remote', False))
    return build_from_cfg(cfg, TRAINERS, group_key=task_name, default_args=default_args)