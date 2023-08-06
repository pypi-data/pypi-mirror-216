import os

from weathon.utils.constants.metainfo import Models
from weathon.models.base.base_torch_model import TorchModel
from weathon.registry import MODELS
from weathon.utils.constants import ModelFile, Tasks


@MODELS.register_module(
    Tasks.image_classification, module_name=Models.classification_model)
class ClassificationModel(TorchModel):

    def __init__(self, model_dir: str, **kwargs):
        import mmcv
        from mmcls.models import build_classifier
        from weathon.utils.hub.utils import read_config

        super().__init__(model_dir)

        self.config_type = 'ms_config'
        mm_config = os.path.join(model_dir, 'config.py')
        if os.path.exists(mm_config):
            cfg = mmcv.Config.fromfile(mm_config)
            cfg.model.pretrained = None
            self.cls_model = build_classifier(cfg.model)
            self.config_type = 'mmcv_config'
        else:
            cfg = read_config(model_dir)
            cfg.model.mm_model.pretrained = None
            self.cls_model = build_classifier(cfg.model.mm_model)
            self.config_type = 'ms_config'
        self.cfg = cfg

        self.ms_model_dir = model_dir

        self.load_pretrained_checkpoint()

    def forward(self, inputs):

        return self.cls_model(**inputs)

    def load_pretrained_checkpoint(self):
        import mmcv
        if os.path.exists(
                os.path.join(self.ms_model_dir, ModelFile.TORCH_MODEL_FILE)):
            checkpoint_path = os.path.join(self.ms_model_dir,
                                           ModelFile.TORCH_MODEL_FILE)
        else:
            checkpoint_path = os.path.join(self.ms_model_dir,
                                           'checkpoints.pth')
        if os.path.exists(checkpoint_path):
            checkpoint = mmcv.runner.load_checkpoint(
                self.cls_model, checkpoint_path, map_location='cpu')
            if 'CLASSES' in checkpoint.get('meta', {}):
                self.cls_model.CLASSES = checkpoint['meta']['CLASSES']
                self.CLASSES = self.cls_model.CLASSES
