import json
from copy import deepcopy
from weathon.utils.torch_utils import is_master
from weathon.utils.fileio.format.json_utils import JSONIteratorEncoder
def print_cfg(self):
    if is_master():
        cfg = deepcopy(self.cfg)
        cfg.train.work_dir = self.work_dir
        self.logger.info('==========================Training Config Start==========================')
        self.logger.info(json.dumps(cfg._cfg_dict, indent=4, cls=JSONIteratorEncoder))
        self.logger.info('===========================Training Config End===========================')