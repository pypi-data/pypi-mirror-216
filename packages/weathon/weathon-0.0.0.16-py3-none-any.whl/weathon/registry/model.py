from weathon.registry.registry import Registry, build_from_cfg
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models
from weathon.utils.config.config import ConfigDict
from weathon.utils.logger import get_logger
from weathon.utils.task_utils import get_task_by_subtask_name

logger = get_logger()

MODELS = Registry('models')
HEADS = Registry('heads')
BACKBONES = MODELS
def register_models():
    from weathon.utils.ast_utils import INDEX_KEY
    from weathon.utils.import_utils import LazyImportModule
    modules = LazyImportModule.AST_INDEX[INDEX_KEY]
    for module_index in list(modules.keys()):
        if module_index[1] == Tasks.backbone and module_index[0] == 'BACKBONES':
            modules[(MODELS.name.upper(), module_index[1], module_index[2])] = modules[module_index]


def build_model(cfg: ConfigDict, task_name: str = None, default_args: dict = None):
    """ build model given model config dict

    Args:
        cfg (:obj:`ConfigDict`): config dict for model object.
        task_name (str, optional):  task name, refer to
            :obj:`Tasks` for more details
        default_args (dict, optional): Default initialization arguments.
    """
    try:
        model = build_from_cfg(cfg, MODELS, group_key=task_name, default_args=default_args)
    except KeyError as e:
        # Handle subtask with a backbone model that hasn't been registered
        # All the subtask with a parent task should have a task model, otherwise it is not a
        # valid subtask
        parent_task, task_model_type = get_task_by_subtask_name(task_name)
        if task_model_type is None:
            raise KeyError(e)
        cfg['type'] = task_model_type
        model = build_from_cfg(cfg, MODELS, group_key=parent_task, default_args=default_args)
    return model


def build_backbone(cfg: ConfigDict, task_name:str = Tasks.backbone, default_args: dict = None):
    """ build backbone given backbone config dict

    Args:
        cfg (:obj:`ConfigDict`): config dict for backbone object.
        default_args (dict, optional): Default initialization arguments.
    """
    if not cfg.get('init_backbone', False):
        model_dir = cfg.pop('model_dir', None)
    else:
        model_dir = cfg.get('model_dir', None)
    try:
        model = build_from_cfg(cfg, BACKBONES, group_key=task_name, default_args=default_args)
    except KeyError:
        # Handle backbone that is not in the register group by using transformers AutoModel.
        # AutoModel are mostly using in NLP and part of Multi-Modal, while the number of backbone in CV、Audio and MM
        # is limited, thus could be added and registered in weathon directly
        logger.warning(f'The backbone {cfg.type} is not registered in weathon, try to import the backbone from hf transformers.')
        cfg['type'] = Models.transformers
        cfg['model_dir'] = model_dir
        model = build_from_cfg(cfg, BACKBONES, group_key=task_name, default_args=default_args)
    return model


def build_head(cfg: ConfigDict, task_name: str = None, default_args: dict = None):
    """ build head given config dict

    Args:
        cfg (:obj:`ConfigDict`): config dict for head object.
        task_name (str, optional):  task name, refer to
            :obj:`Tasks` for more details
        default_args (dict, optional): Default initialization arguments.
    """
    return build_from_cfg(cfg, HEADS, group_key=task_name, default_args=default_args)



register_models