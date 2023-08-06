"""UniTE model configuration"""

from enum import Enum

from weathon.utils import logger as logging
from weathon.utils.config.config import Config

logger = logging.get_logger()


class InputFormat(Enum):
    SRC = 'src'
    REF = 'ref'
    SRC_REF = 'src-ref'


class UniTEConfig(Config):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
