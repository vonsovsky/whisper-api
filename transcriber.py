from typing import Optional, Tuple

import numpy as np
import whisper


def batch_audio(audio_arr, sec: int, sr: int):
    k = sec * sr
    for i in range(0, len(audio_arr), k):
        yield audio_arr[i:i + k]


class Transcriber:

    def __init__(self, model_name: str):
        self.model = whisper.load_model(model_name)
        self.n_mels = 80
        if model_name == "large":
            self.n_mels = 128
        self.default_sr = 16_000
        self.fp16 = False  # TODO should be True if GPU

    def transcribe_file(
            self,
            file_path: str,
            start: Optional[float] = None,
            end: Optional[float] = None,
            sr: Optional[int] = None,
    ) -> str:
        """
        Transcribe file on hard drive
        :param file_path: File path
        :param start: Start in minutes, optional
        :param end: End in minutes, optional
        :param sr: Sample rate
        :return: Transcribed text
        """
        if sr is None:
            sr = self.default_sr

        audio = whisper.load_audio(file_path, sr=sr)
        return self.transcribe_audio(audio, start, end, sr)

    def transcribe_audio(
            self,
            audio: np.ndarray,
            start: Optional[float] = None,
            end: Optional[float] = None,
            sr: Optional[int] = None,
    ) -> str:
        """
        Transcribe audio samples
        :param audio: Samples in numpy float32
        :param start: Start in minutes, optional
        :param end: End in minutes, optional
        :param sr: Sample rate
        :return: Transcribed text
        """

        if sr is None:
            sr = self.default_sr

        # convert to mono if stereo as required by whisper
        if len(audio.shape) == 2:
            # channels always first
            if audio.shape[1] < audio.shape[0]:
                audio = audio.T
            audio = np.mean(audio, axis=0)

        if len(audio.shape) > 2:
            raise ValueError("Too many dimensions")

        if end is not None:
            audio = audio[:int(sr * 60 * end)]
        if start is not None:
            audio = audio[int(sr * 60 * start):]

        result_text = ""
        for audio_chunk in batch_audio(audio, 30, sr):
            _, batch_tr = self.transcribe_audio_chunk(audio_chunk)
            print(batch_tr)
            result_text += batch_tr + "\n"

        return result_text

    def transcribe_audio_chunk(
            self,
            audio_chunk: np.ndarray,
            sr: Optional[int] = None
    ) -> Tuple[str, str]:
        if sr is None:
            sr = self.default_sr
        if audio_chunk.shape[0] < sr * whisper.audio.CHUNK_LENGTH:
            audio_chunk = whisper.pad_or_trim(audio_chunk)

        mel = (whisper.log_mel_spectrogram(audio_chunk, n_mels=self.n_mels)
               .to(self.model.device))

        _, probs = self.model.detect_language(mel)
        lang = max(probs, key=probs.get)

        options = whisper.DecodingOptions(fp16=self.fp16)
        result = whisper.decode(self.model, mel, options)

        return lang, result.text
