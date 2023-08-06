
from weathon.registry.registry import Registry, build_from_cfg
from weathon.utils.config.config import ConfigDict

PIPELINES = Registry('pipelines')

def build_pipeline(cfg: ConfigDict,task_name: str = None,default_args: dict = None):
    """ build pipeline given model config dict.

    Args:
        cfg (:obj:`ConfigDict`): config dict for model object.
        task_name (str, optional):  task name, refer to
            :obj:`Tasks` for more details.
        default_args (dict, optional): Default initialization arguments.
    """
    return build_from_cfg(cfg, PIPELINES, group_key=task_name, default_args=default_args)