from typing import Union, Dict, Mapping

from weathon.utils.config.config import ConfigDict
from weathon.registry.registry import Registry, default_group, build_from_cfg


METRICS = Registry('metrics')


def build_metric(metric_cfg: Union[str, Dict],task_name: str = default_group,default_args: dict = None):
    """ Build metric given metric_name and field.

    Args:
        metric_name (str | dict): The metric name or metric config dict.
        field (str, optional):  The field of this metric, default value: 'default' for all fields.
        default_args (dict, optional): Default initialization arguments.
    """
    if isinstance(metric_cfg, Mapping):
        assert 'type' in metric_cfg
    else:
        metric_cfg = ConfigDict({'type': metric_cfg})
    return build_from_cfg(metric_cfg, METRICS, group_key=task_name, default_args=default_args)