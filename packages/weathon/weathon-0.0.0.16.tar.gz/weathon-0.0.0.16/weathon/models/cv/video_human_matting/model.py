import os.path as osp

import numpy as np
import torch

from weathon.utils.constants.metainfo import Models
from weathon.models.base import TorchModel
from weathon.registry import MODELS
from weathon.models.cv.video_human_matting.models import MattingNetwork
from weathon.utils.constants import ModelFile, Tasks


@MODELS.register_module(
    Tasks.video_human_matting, module_name=Models.video_human_matting)
class VideoMattingNetwork(TorchModel):

    def __init__(self, model_dir: str, *args, **kwargs):
        super().__init__(model_dir, *args, **kwargs)
        model_path = osp.join(model_dir, ModelFile.TORCH_MODEL_FILE)
        params = torch.load(model_path, map_location='cpu')
        self.model = MattingNetwork()
        if 'model_state_dict' in params.keys():
            params = params['model_state_dict']
        self.model.load_state_dict(params, strict=True)
        self.model.eval()


def preprocess(image):
    frame_np = np.float32(image) / 255.0
    frame_np = frame_np.transpose(2, 0, 1)
    frame_tensor = torch.from_numpy(frame_np)
    image_tensor = frame_tensor[None, :, :, :]
    return image_tensor
