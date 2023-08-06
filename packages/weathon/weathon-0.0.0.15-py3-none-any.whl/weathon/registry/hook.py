from weathon.registry.registry import Registry,build_from_cfg, default_group


HOOKS = Registry('hooks')


def build_hook(cfg,task_name:str=default_group, default_args=None):
    return build_from_cfg(cfg, HOOKS, group_key=task_name, default_args=default_args)