import os

import torch

from weathon.utils.constants.metainfo import Models
from weathon.models.base.base_torch_model import TorchModel
from weathon.registry import MODELS
from weathon.utils.constants import Tasks


@MODELS.register_module(
    Tasks.crowd_counting, module_name=Models.crowd_counting)
class HRNetCrowdCounting(TorchModel):

    def __init__(self, model_dir: str, **kwargs):
        super().__init__(model_dir, **kwargs)

        from .hrnet_aspp_relu import HighResolutionNet as HRNet_aspp_relu

        domain_center_model = os.path.join(
            model_dir, 'average_clip_domain_center_54.97.npz')
        net = HRNet_aspp_relu(
            attn_weight=1.0,
            fix_domain=0,
            domain_center_model=domain_center_model)
        net.load_state_dict(
            torch.load(
                os.path.join(model_dir, 'DCANet_final.pth'),
                map_location='cpu'))
        self.model = net

    def forward(self, inputs):
        return self.model(inputs)
