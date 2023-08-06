from dataclasses import dataclass

from weathon.base import BaseModelOutput
from weathon.utils.typing import Tensor


@dataclass
class DetectionOutput(BaseModelOutput):
    """The output class for object detection models.

    Args:
        class_ids (`Tensor`, *optional*): class id for each object.
        boxes (`Tensor`, *optional*): Bounding box for each detected object in  [left, top, right, bottom] format.
        scores (`Tensor`, *optional*): Detection score for each object.
        keypoints (`Tensor`, *optional*): Keypoints for each object using four corner points in a 8-dim tensor
            in the order of (x, y) for each corner point.

    """

    class_ids: Tensor = None
    scores: Tensor = None
    boxes: Tensor = None
    keypoints: Tensor = None

