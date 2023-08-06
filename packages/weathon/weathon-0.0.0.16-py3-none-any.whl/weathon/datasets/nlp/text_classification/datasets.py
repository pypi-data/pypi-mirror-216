from typing import Optional

import pandas as pd
import os.path as osp

from weathon.base.dataset import TorchCustomDataset
from weathon.registry import CUSTOM_DATASETS
from weathon.utils.config.config import ConfigDict
from weathon.utils.constants import Tasks, Datasets


@CUSTOM_DATASETS.register_module(group_key=Tasks.text_classification, module_name=Datasets.jd_sentiment_text_classification)
class JDTextClassificationDataset(TorchCustomDataset):

    def __init__(self, dataset_cfg: Optional[ConfigDict] = None,*args, **kwargs):
        dataset_cfg = dataset_cfg if dataset_cfg else dict()
        self.data_dir = kwargs.get("data_dir", dataset_cfg.get("data_dir",None))
        self.filename = kwargs.get("file",dataset_cfg.get("file",None))
        self.label2id = kwargs.get("label2id",dataset_cfg.get("label2id",None))
        self.id2label = kwargs.get("id2label", dataset_cfg.get("id2label", None))
        self.preprocessor = kwargs.get("preprocessor",dataset_cfg.get("preprocessor",None))
        self.examples = self.get_examples()

    def get_examples(self):
        data_pd = pd.read_csv(osp.join(self.data_dir, self.filename))
        data_pd = data_pd.dropna()
        data_pd = data_pd[(data_pd["label"] != None) & (data_pd["sentence"] != None)]
        data_pd["label"] = data_pd["label"].apply(lambda x: self.label2id[int(x)])
        examples = [{**item} for idx, item in data_pd.iterrows()]
        return examples

    def __getitem__(self, index):
        return self.preprocessor(self.examples[index]) if self.preprocessor else self.examples[index]

    def __len__(self):
        return len(self.examples)
