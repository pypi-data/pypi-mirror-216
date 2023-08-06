from typing import Optional,List

import cv2
import numpy as np
import os.path as osp

from weathon.base.dataset import TorchCustomDataset
from weathon.registry import CUSTOM_DATASETS
from weathon.utils.config.config import ConfigDict
from weathon.utils.constants import Tasks,Datasets


@CUSTOM_DATASETS.register_module(group_key=Tasks.ocr_detection, module_name=Datasets.icdar2015_ocr_detection)
class IcdarOcrDetectionDataset(TorchCustomDataset):

    def __init__(self, dataset_cfg:Optional[ConfigDict] = None, *args, **kwargs):
        dataset_cfg = dataset_cfg if dataset_cfg else dict()
        self.data_dir = kwargs.get("data_dir", dataset_cfg.get("data_dir",None))
        self.label_file = kwargs.get("label_file", dataset_cfg.get("label_file", None))
        self.preprocessor = kwargs.get("preprocessor",dataset_cfg.get("preprocessor",None))
        self.examples = self._get_examples()

    def _get_examples(self):
        examples = []
        with open(osp.join(self.data_dir, self.label_file), "r", encoding="utf8") as reader:
            for line in reader:
                image_file, line_labels = line.split("\t",maxsplit=1)
                labels = self._parse_line_label(line_labels)
                image_path = osp.join(self.data_dir, image_file)
                img = cv2.imread(image_path, cv2.IMREAD_COLOR).astype('float32')
                examples.append({
                    "filename": image_path,
                    "data_id": image_path,
                    "image": img,
                    "lines": labels
                })
        return examples

    def _parse_line_label(self,line_labels:str) -> List:
        # [{"transcription": "MASA", "points": [[310, 104], [416, 141], [418, 216], [312, 179]]}, {"transcription": "###", "points": [[1197, 126], [1252, 118], [1257, 136], [1203, 144]]}, {"transcription": "###", "points": [[1137, 140], [1177, 132], [1180, 148], [1140, 156]]}, {"transcription": "###", "points": [[1096, 152], [1130, 145], [1133, 158], [1100, 165]]}, {"transcription": "###", "points": [[1061, 161], [1092, 154], [1093, 168], [1062, 175]]}, {"transcription": "###", "points": [[1030, 168], [1055, 162], [1056, 177], [1030, 183]]}, {"transcription": "###", "points": [[1000, 173], [1023, 168], [1025, 184], [1002, 189]]}, {"transcription": "###", "points": [[223, 293], [313, 288], [313, 311], [222, 316]]}]
        labels = []
        label_list = eval(line_labels)
        for label in label_list:
            if label["transcription"] == "###":
                continue
            labels.append({
                "text": label["transcription"],
                "poly": np.array(label["points"],dtype=np.float32)
            })
        return labels


    
    def __getitem__(self, index):
        return self.preprocessor(self.examples[index]) if self.preprocessor else self.examples[index]

    def __len__(self):
        return len(self.examples)
