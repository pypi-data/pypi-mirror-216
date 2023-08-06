from weathon.utils.config.config import ConfigDict
from weathon.registry.registry import build_from_cfg,Registry


CUSTOM_DATASETS = Registry('custom_datasets')


def build_custom_dataset(cfg: ConfigDict,task_name: str, default_args: dict = None):
    """
        给定模型配置文件 以及 任务名称 构建用户自定义数据集
    Args:
        cfg (:obj:`ConfigDict`): config dict for model object.
        task_name (str, optional):  task name, refer to
            :obj:`Tasks` for more details
        default_args (dict, optional): Default initialization arguments.
    """
    return build_from_cfg(cfg, CUSTOM_DATASETS, group_key=task_name, default_args=default_args)