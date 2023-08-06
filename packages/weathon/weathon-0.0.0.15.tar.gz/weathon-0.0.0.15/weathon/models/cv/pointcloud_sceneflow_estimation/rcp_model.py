import os.path as osp

import numpy as np
import torch

from weathon.utils.constants.metainfo import Models
from weathon.models.base.base_torch_model import TorchModel
from weathon.registry import MODELS
from weathon.outputs import OutputKeys
from weathon.utils.constants import ModelFile, Tasks
from weathon.utils.logger import get_logger
from .sf_rcp import SF_RCP

logger = get_logger()


@MODELS.register_module(
    Tasks.pointcloud_sceneflow_estimation,
    module_name=Models.rcp_sceneflow_estimation)
class SceneFlowEstimation(TorchModel):

    def __init__(self, model_dir: str, **kwargs):
        """str -- model file root."""
        super().__init__(model_dir, **kwargs)

        assert torch.cuda.is_available(
        ), 'current model only support run in gpu'

        # build model
        self.model = SF_RCP(
            npoint=8192,
            use_instance_norm=False,
            model_name='SF_RCP',
            use_insrance_norm=False,
            use_curvature=True)

        # load model
        model_path = osp.join(model_dir, ModelFile.TORCH_MODEL_FILE)

        logger.info(f'load ckpt from:{model_path}')

        checkpoint = torch.load(model_path, map_location='cpu')

        self.model.load_state_dict({k: v for k, v in checkpoint.items()})
        self.model.cuda()
        self.model.eval()

    def forward(self, Inputs):

        return self.model(Inputs['pcd1'], Inputs['pcd2'], Inputs['pcd1'],
                          Inputs['pcd2'])[-1]

    def postprocess(self, Inputs):
        output = Inputs['output']

        results = {OutputKeys.OUTPUT: output.detach().cpu().numpy()[0]}

        return results

    def inference(self, data):
        results = self.forward(data)

        return results
