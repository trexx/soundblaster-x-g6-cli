import json
from typing import Any

from g6_cli.g6_model.decoder import Decoder
from g6_cli.g6_model.serialization import DeserializationError, SerializationError
from g6_cli.g6_model.lighting import Lighting
from g6_cli.g6_model.mixer import Mixer
from g6_cli.g6_model.playback import Playback
from g6_cli.g6_model.recording import Recording
from g6_cli.g6_model.sbx import SBX


class G6Model:
    """
    Model class holding the complete settable state of the Sound Blaster G6.
    Each audio component is implemented as a nested subclass.
    All fields are private (__ prefix) and only accessible through getters/setters.
    Supports full JSON serialization/deserialization.
    """

    def __init__(self):
        self.__decoder: Decoder = Decoder()
        self.__sbx: SBX = SBX()
        self.__playback: Playback = Playback()
        self.__recording: Recording = Recording()
        self.__lighting: Lighting = Lighting()
        self.__mixer: Mixer = Mixer()

    def get_decoder(self) -> Decoder:
        return self.__decoder

    def get_sbx(self) -> SBX:
        return self.__sbx

    def get_playback(self) -> Playback:
        return self.__playback

    def get_recording(self) -> Recording:
        return self.__recording

    def get_lighting(self) -> Lighting:
        return self.__lighting

    def get_mixer(self) -> Mixer:
        return self.__mixer

    def to_dict(self) -> dict:
        return {
            "decoder": self.__decoder.to_dict(),
            "sbx": self.__sbx.to_dict(),
            "playback": self.__playback.to_dict(),
            "recording": self.__recording.to_dict(),
            "lighting": self.__lighting.to_dict(),
            "mixer": self.__mixer.to_dict(),
        }

    def to_json(self, file_path: str) -> None:
        """
        Serialize the complete model to a JSON file.
        """
        try:
            data = self.to_dict()
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise SerializationError(e)

    @classmethod
    def from_json(cls, file_path: str) -> "G6Model":
        """
        Deserialize a model from a JSON file (created by to_json).
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data: dict[str, Any] = json.load(f)

            model = cls()
            model.__decoder = Decoder.from_dict(data.get("decoder", {}))
            model.__sbx = SBX.from_dict(data.get("sbx", {}))
            model.__playback = Playback.from_dict(data.get("playback", {}))
            model.__recording = Recording.from_dict(data.get("recording", {}))
            model.__lighting = Lighting.from_dict(data.get("lighting", {}))
            model.__mixer = Mixer.from_dict(data.get("mixer", {}))
            return model
        except Exception as e:
            raise DeserializationError(e)
