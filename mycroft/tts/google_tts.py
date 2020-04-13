# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from gtts import gTTS
from gtts.lang import tts_langs

from .tts import TTS, TTSValidator


class GoogleTTS(TTS):
    """Interface to google TTS."""
    def __init__(self, lang, config):
        super(GoogleTTS, self).__init__(lang, config, GoogleTTSValidator(
            self), 'mp3')

    def get_tts(self, sentence, wav_file):
        """Fetch tts audio using gTTS.

        Arguments:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
        Returns:
            Tuple ((str) written file, None)
        """
        langs = tts_langs()
        if self.lang.lower() not in langs:
            if self.lang[:2].lower() in langs:
                self.lang = self.lang[:2]
            else:
                raise ValueError("Language not supported by gTTS: {}"
                                 .format(self.lang))
        tts = gTTS(text=sentence, lang=self.lang)
        tts.save(wav_file)
        return (wav_file, None)  # No phonemes


class GoogleTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(GoogleTTSValidator, self).__init__(tts)

    def validate_lang(self):
        # TODO
        pass

    def validate_connection(self):
        try:
            gTTS(text='Hi').save(self.tts.filename)
        except Exception:
            raise Exception(
                'GoogleTTS server could not be verified. Please check your '
                'internet connection.')

    def get_tts_class(self):
        return GoogleTTS
