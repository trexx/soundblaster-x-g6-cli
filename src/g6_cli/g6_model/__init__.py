import json
from typing import Any

from g6_cli.g6_model.decoder import Decoder
from g6_cli.g6_model.lighting import Lighting
from g6_cli.g6_model.mixer import Mixer
from g6_cli.g6_model.playback import Playback
from g6_cli.g6_model.recording import Recording
from g6_cli.g6_model.sbx import SBX, Profile, Profiles


class SerializationError(Exception):
    def __init__(self, cause: Exception):
        super().__init__(f"Unable to serialize model: {cause}")


class DeserializationError(Exception):
    def __init__(self, cause: Exception) -> None:
        super().__init__(f"Unable to deserialize model: {cause}")


class G6Model:
    """
    Model class holding the complete settable state of the Sound Blaster G6.
    Each audio component is implemented as a nested subclass.
    All fields are private (__ prefix) and only accessible through getters/setters.
    Supports full JSON serialization/deserialization.
    """

    def __init__(self):
        self.__profiles = Profiles.default()
        self.__decoder: Decoder = Decoder.default()
        self.__playback: Playback = Playback.default()
        self.__recording: Recording = Recording.default()
        self.__lighting: Lighting = Lighting.default()
        self.__mixer: Mixer = Mixer.default()

    def get_sbx_profile_selection(self) -> Profile.Name | None:
        return self.__profiles.get_sbx_profile_selection()

    def set_sbx_profile_selection(self, profile_name: Profile.Name) -> None:
        self.__profiles.set_sbx_profile_selection(profile_name=profile_name)

    def get_sbx(self, profile_name: Profile.Name) -> SBX:
        return self.__profiles.get_sbx(profile_name=profile_name)

    def get_decoder(self) -> Decoder:
        return self.__decoder

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
            "profiles": self.__profiles.to_dict(),
            "decoder": self.__decoder.to_dict(),
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
            model.__profiles = Profiles.from_dict(data.get("profiles", {}))
            model.__decoder = Decoder.from_dict(data.get("decoder", {}))
            model.__playback = Playback.from_dict(data.get("playback", {}))
            model.__recording = Recording.from_dict(data.get("recording", {}))
            model.__lighting = Lighting.from_dict(data.get("lighting", {}))
            model.__mixer = Mixer.from_dict(data.get("mixer", {}))
            return model
        except Exception as e:
            raise DeserializationError(e)
