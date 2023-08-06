import os

from kantts.preprocess.data_process import process_data

from weathon.base import BasePreprocessor
from weathon.registry import PREPROCESSORS
from weathon.utils.constants.metainfo import Preprocessors
from weathon.utils.audio.tts_exceptions import ( TtsDataPreprocessorAudioConfigNotExistsException, TtsDataPreprocessorDirNotExistsException)
from weathon.utils.constants import Tasks

__all__ = ['KanttsDataPreprocessor']


@PREPROCESSORS.register_module(
    group_key=Tasks.text_to_speech,
    module_name=Preprocessors.kantts_data_preprocessor)
class KanttsDataPreprocessor(BasePreprocessor):

    def __init__(self):
        pass

    def __call__(self,
                 data_dir,
                 output_dir,
                 audio_config_path,
                 speaker_name='F7',
                 target_lang='PinYin',
                 skip_script=False,
                 se_model=None):
        self.do_data_process(data_dir, output_dir, audio_config_path,
                             speaker_name, target_lang, skip_script, se_model)

    def do_data_process(self,
                        datadir,
                        outputdir,
                        audio_config,
                        speaker_name='F7',
                        targetLang='PinYin',
                        skip_script=False,
                        se_model=None):
        if not os.path.exists(datadir):
            raise TtsDataPreprocessorDirNotExistsException(
                'Preprocessor: dataset dir not exists')
        if not os.path.exists(outputdir):
            raise TtsDataPreprocessorDirNotExistsException(
                'Preprocessor: output dir not exists')
        if not os.path.exists(audio_config):
            raise TtsDataPreprocessorAudioConfigNotExistsException(
                'Preprocessor: audio config not exists')
        process_data(datadir, outputdir, audio_config, speaker_name,
                     targetLang, skip_script, se_model)
