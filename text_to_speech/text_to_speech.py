import wave
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException
import json
import pyttsx3
import os
import io
import pyaudio


class Speech(object):
    def __init__(self, rate=200, volume=1.0):
        self.engine = pyttsx3.init()
        self._rate = rate
        self._volume = volume
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def speech_list(self, text_strings, new_rate=None, new_volume=None):
        if new_rate:
            self.rate = new_rate
        if new_volume:
            self.volume = new_volume
        for sen in text_strings:
            self.engine.say(sen)
        self.engine.runAndWait()

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, new_rate):
        if 0 <= new_rate <= 500:
            self._rate = new_rate
            self.engine.setProperty('rate', new_rate)
            # print(new_rate, self.engine.getProperty('rate'))
        else:
            raise ValueError("The new rate should be 0 - 500")

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, new_volume):
        if 0 <= new_volume <= 1:
            self._volume = new_volume
            self.engine.setProperty('volume', new_volume)
        else:
            raise ValueError("The new rate should be 0 - 1")


class SpeechIBM(object):
    def __init__(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'config_exe.json')) as config_file:
            speech_api = json.load(config_file)['speech_api']

        authenticator = IAMAuthenticator(speech_api)
        self.text_to_speech = TextToSpeechV1(
            authenticator=authenticator
        )

        self.text_to_speech.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com')

        self.pya = pyaudio.PyAudio()

    def speech(self, text_string, rate_speech=22050):

        sound_bytes = self.text_to_speech.synthesize(
            text=text_string,
            voice='en-GB_JamesV3Voice',
            accept='audio/wav'
        ).get_result().content

        stream = self.pya.open(format=self.pya.get_format_from_width(width=2), channels=1, rate=rate_speech, output=True)
        stream.write(sound_bytes)
        stream.stop_stream()
        stream.close()

    def speechLocal(self, text_string, file_name):
        with open(os.path.join(os.path.dirname(__file__), 'reminder_voices', file_name + '.wav'), 'wb') as fp:
            fp.write(
                self.text_to_speech.synthesize(
                    text=text_string,
                    voice='en-GB_JamesV3Voice',
                    accept='audio/wav'
                ).get_result().content)


if __name__ == "__main__":
    s = SpeechIBM()
    s.speech("This is a test. you can adjust the rate of video")
    s.speechLocal("This is a test. you can adjust the rate of video", 'test_file')
