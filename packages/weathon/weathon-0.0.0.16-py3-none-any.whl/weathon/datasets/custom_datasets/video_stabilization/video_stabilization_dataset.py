from weathon.base import TorchCustomDataset
from weathon.registry import CUSTOM_DATASETS
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models


@CUSTOM_DATASETS.register_module(Tasks.video_stabilization, module_name=Models.video_stabilization)
class VideoStabilizationDataset(TorchCustomDataset):
    """Paired video dataset for video stabilization.
    """

    def __init__(self, dataset, opt):
        self.dataset = dataset
        self.opt = opt

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):

        # Load input video paths.
        item_dict = self.dataset[index]
        input_path = item_dict['input_video:FILE']

        return {'input': input_path}
