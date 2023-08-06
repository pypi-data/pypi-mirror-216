from typing import Union

from weathon.utils.config.config import ConfigDict, Config
from weathon.utils.constants import ModelFile, ConfigFields


def check_config(cfg: Union[str, ConfigDict], is_training=False):
    """ Check whether configuration file is valid, If anything wrong, exception will be raised.

    Args:
        cfg (str or ConfigDict): Config file path or config object.
        is_training: indicate if checking training related elements
    """

    if isinstance(cfg, str):
        cfg = Config.from_file(cfg)

    def check_attr(attr_name, msg=''):
        assert hasattr(cfg, attr_name), f'Attribute {attr_name} is missing from ' \
            f'{ModelFile.CONFIGURATION}. {msg}'

    check_attr(ConfigFields.framework)
    check_attr(ConfigFields.task)
    check_attr(ConfigFields.pipeline)

    if is_training:
        check_attr(ConfigFields.model)
        check_attr(ConfigFields.train)
        check_attr(ConfigFields.preprocessor)
        check_attr(ConfigFields.evaluation)