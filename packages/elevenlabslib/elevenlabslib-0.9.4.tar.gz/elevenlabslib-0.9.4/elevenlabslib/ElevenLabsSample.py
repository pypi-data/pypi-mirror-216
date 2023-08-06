from __future__ import annotations
from elevenlabslib.ElevenLabsVoice import ElevenLabsVoice
from elevenlabslib.helpers import *
from elevenlabslib.helpers import _api_json,_api_del,_api_get,_api_multipart

class ElevenLabsSample:
    """
    Represents a sample used for a cloned voice.
    """
    def __init__(self, sampleData, parentVoice:ElevenLabsVoice):
        self._parentVoice = parentVoice
        self._sampleID = sampleData["sample_id"]
        self._fileName = sampleData["file_name"]
        self._fullMetaData = sampleData
        self._mimeType = sampleData["mime_type"]
        self._size = sampleData["size_bytes"]
        self._hash = sampleData["hash"]
        self._audioData = None      #This is used to cache the audio data since it never changes.

    @property
    def metadata(self):
        """
        The full metadata associated with the sample.
        """
        return self._fullMetaData

    @property
    def parentVoice(self):
        """
        The ElevenLabsVoice object associated with this sample.
        """
        return self._parentVoice

    @property
    def sampleID(self):
        """
        The unique sampleID.
        """
        return self._sampleID

    @property
    def fileName(self):
        """
        The filename of the sample.
        """
        return self._fileName

    def get_audio_bytes(self) -> bytes:
        """
        Retrieves the audio bytes associated with the sample.

        Note:
            The audio will be cached so that it's not downloaded every time this is called.

        Returns:
            bytes: a bytes object containing the audio in mp3 format.
        """
        if self._audioData is None:
            response = _api_get("/voices/" + self._parentVoice.voiceID + "/samples/" + self._sampleID + "/audio", self._parentVoice.linkedUser.headers)
            self._audioData = response.content
        return self._audioData

    def play_audio(self, playInBackground: bool, portaudioDeviceID: Optional[int] = None,
                     onPlaybackStart:Callable=lambda: None, onPlaybackEnd:Callable=lambda: None) -> sd.OutputStream:
        """
        Downloads and plays the audio associated with the sample.

        Args:
            playInBackground: a boolean indicating whether the audio should be played in the background
            portaudioDeviceID: an optional integer representing the portaudio device ID to use
            onPlaybackStart: Function to call once the playback begins
            onPlaybackEnd: Function to call once the playback ends
        """
        return play_audio_bytes(self.get_audio_bytes(), playInBackground, portaudioDeviceID, onPlaybackStart, onPlaybackEnd)


    def delete(self):
        """
        Deletes the sample.
        """
        response = _api_del("/voices/" + self._parentVoice.voiceID + "/samples/" + self._sampleID, self._parentVoice.linkedUser.headers)
        self._sampleID = ""

