from abc import ABC, abstractmethod

from weathon.utils.config.dataset_context_config import DatasetContextConfig


class BaseDownloader(ABC):
    """Base dataset downloader to load data."""

    def __init__(self, dataset_context_config: DatasetContextConfig):
        self.dataset_context_config = dataset_context_config

    @abstractmethod
    def process(self):
        """The entity processing pipeline for fetching the data. """
        raise NotImplementedError(
            f'No default implementation provided for {BaseDownloader.__name__}.process.'
        )

    @abstractmethod
    def _authorize(self):
        raise NotImplementedError(
            f'No default implementation provided for {BaseDownloader.__name__}._authorize.'
        )

    @abstractmethod
    def _build(self):
        raise NotImplementedError(
            f'No default implementation provided for {BaseDownloader.__name__}._build.'
        )

    @abstractmethod
    def _prepare_and_download(self):
        raise NotImplementedError(
            f'No default implementation provided for {BaseDownloader.__name__}._prepare_and_download.'
        )

    @abstractmethod
    def _post_process(self):
        raise NotImplementedError(
            f'No default implementation provided for {BaseDownloader.__name__}._post_process.'
        )
