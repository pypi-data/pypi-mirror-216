from torch.nn.parallel.distributed import DistributedDataParallel

from weathon.registry.registry import Registry, build_from_cfg
from weathon.utils.config.config import ConfigDict

PARALLEL = Registry('parallel')
PARALLEL.register_module(module_name='DistributedDataParallel', module_cls=DistributedDataParallel)


def build_parallel(cfg: ConfigDict, default_args: dict = None):
    """ build parallel

    Args:
        cfg (:obj:`ConfigDict`): config dict for parallel object.
        default_args (dict, optional): Default initialization arguments.
    """
    return build_from_cfg(cfg, PARALLEL, default_args=default_args)
