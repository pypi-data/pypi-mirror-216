import os
from typing import Any, Dict

import json
import wenetruntime as wenet

from weathon.base import BaseModel
from weathon.registry import MODELS
from weathon.utils.constants import Tasks
from weathon.utils.constants.metainfo import Models


__all__ = ['WeNetAutomaticSpeechRecognition']


@MODELS.register_module(Tasks.auto_speech_recognition, module_name=Models.wenet_asr)
class WeNetAutomaticSpeechRecognition(BaseModel):

    def __init__(self, model_dir: str, am_model_name: str,
                 model_config: Dict[str, Any], *args, **kwargs):
        """initialize the info of model.

        Args:
            model_dir (str): the model path.
        """
        super().__init__(model_dir, am_model_name, model_config, *args,
                         **kwargs)
        self.decoder = wenet.Decoder(model_dir, lang='chs')

    def forward(self, inputs: Dict[str, Any]) -> str:
        if inputs['audio_format'] == 'wav':
            rst = self.decoder.decode_wav(inputs['audio'])
        else:
            rst = self.decoder.decode(inputs['audio'])
        text = json.loads(rst)['nbest'][0]['sentence']
        return {'text': text}
