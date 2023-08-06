from typing import Dict, List, Tuple, Union

from weathon.base import BaseModel
Model = Union[BaseModel, str]
Image = Union[str, 'Image.Image', 'numpy.ndarray']
Text = str
Audio = Union[str, bytes, 'np.ndarray']
Video = Union[str, 'np.ndarray', 'cv2.VideoCapture']

Tensor = Union['torch.Tensor', 'tf.Tensor']

Input = Union[Dict[str, Tensor], BaseModel]