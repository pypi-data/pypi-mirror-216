import time

from weathon.base import BaseHook
from weathon.registry import HOOKS
from weathon.utils.constants import Priority, LogKeys
from weathon.utils.constants.metainfo import Hooks



@HOOKS.register_module(module_name=Hooks.IterTimerHook)
class IterTimerHook(BaseHook):
    PRIORITY = Priority.LOW

    def before_epoch(self, trainer):
        self.start_time = time.time()

    def before_iter(self, trainer):
        trainer.log_buffer.update({LogKeys.DATA_LOAD_TIME: time.time() - self.start_time})

    def after_iter(self, trainer):
        trainer.log_buffer.update(
            {LogKeys.ITER_TIME: time.time() - self.start_time})
        self.start_time = time.time()
