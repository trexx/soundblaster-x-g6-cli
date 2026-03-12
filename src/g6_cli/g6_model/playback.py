from enum import Enum

from g6_cli.g6_model.serialization import deserialize_channel, serialize_channel
from g6_cli.g6_spec import Channel, PlaybackFilter, BOTH_CHANNELS


class AudioMode(Enum):
    AM_STEREO = 'Stereo'
    AM_5_1 = '5.1'
    AM_7_1 = '7.1'


class Playback:
    """Playback audio component."""

    def __init__(self):
        self.__mute: bool = False
        self.__is_speakers: bool = True
        self.__speakers_audio_mode: AudioMode = AudioMode.AM_STEREO
        self.__headphones_audio_mode: AudioMode = AudioMode.AM_STEREO
        self.__volumes: dict[Channel, int] = {channel: 50 for channel in BOTH_CHANNELS}
        self.__direct_mode_enabled: bool = False
        self.__spdif_out_direct_mode_enabled: bool = False
        self.__filter: PlaybackFilter = list(PlaybackFilter)[0]

    def get_mute(self) -> bool:
        """
        Get playback mute state.
        """
        return self.__mute

    def set_mute(self, mute: bool) -> None:
        """
        Set playback mute state.
        """
        self.__mute = mute

    def get_is_speakers(self) -> bool:
        """
        Get whether output is toggled to speakers (True) or headphones (False).
        """
        return self.__is_speakers

    def set_is_speakers(self, is_speakers: bool) -> None:
        """
        Set output target (speakers or headphones).
        """
        self.__is_speakers = is_speakers

    def get_speakers_audio_mode(self) -> AudioMode:
        """
        Get the speakers audio mode.
        """
        return self.__speakers_audio_mode

    def set_speakers_audio_mode(self, audio_mode: AudioMode) -> None:
        """
        Set the speakers audio mode.
        """
        self.__speakers_audio_mode = audio_mode

    def get_headphones_audio_mode(self) -> AudioMode:
        """
        Get the headphones audio mode.
        """
        return self.__headphones_audio_mode

    def set_headphones_audio_mode(self, audio_mode: AudioMode) -> None:
        """
        Set the headphones audio mode.
        """
        self.__headphones_audio_mode = audio_mode

    def get_volume(self, channel: Channel) -> int:
        """
        Get playback volume for a specific channel.
        """
        return self.__volumes.get(channel, 50)

    def set_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        """
        Set playback volume.
        """
        if volume_percent < 0 or volume_percent > 100:
            raise ValueError(f"Volume percentage must be between 0 and 100, got {volume_percent}")
        if volume_percent % 10 != 0:
            raise ValueError(f"Volume percentage must be a multiple of 10, got {volume_percent}")
        for channel in channels:
            if channel in self.__volumes:
                self.__volumes[channel] = volume_percent

    def get_direct_mode_enabled(self) -> bool:
        """
        Get direct mode enabled state.
        """
        return self.__direct_mode_enabled

    def set_direct_mode_enabled(self, enable: bool) -> None:
        """
        Set direct mode enabled state.
        """
        self.__direct_mode_enabled = enable

    def get_spdif_out_direct_mode_enabled(self) -> bool:
        """
        Get SPDIF-Out direct mode enabled state.
        """
        return self.__spdif_out_direct_mode_enabled

    def set_spdif_out_direct_mode_enabled(self, enable: bool) -> None:
        """
        Set SPDIF-Out direct mode enabled state.
        """
        self.__spdif_out_direct_mode_enabled = enable

    def get_filter(self) -> PlaybackFilter:
        """
        Get playback filter.
        """
        return self.__filter

    def set_filter(self, playback_filter_enum: PlaybackFilter) -> None:
        """
        Set playback filter.
        """
        if not isinstance(playback_filter_enum, PlaybackFilter):
            raise ValueError(f"playback_filter_enum must be PlaybackFilter, got {type(playback_filter_enum)}")
        self.__filter = playback_filter_enum

    def to_dict(self) -> dict:
        return {
            "mute": self.__mute,
            "is_speakers": self.__is_speakers,
            "speakers_audio_mode": self.__speakers_audio_mode.value,
            "headphones_audio_mode": self.__headphones_audio_mode.value,
            "volumes": {serialize_channel(channel=ch): v for ch, v in sorted(self.__volumes.items())},
            "direct_mode_enabled": self.__direct_mode_enabled,
            "spdif_out_direct_mode_enabled": self.__spdif_out_direct_mode_enabled,
            "filter": self.__filter.name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Playback":
        def deserialize_audio_mode(audio_mode_text: str) -> AudioMode:
            for audio_mode in AudioMode:
                if audio_mode_text == audio_mode.value:
                    return audio_mode
            raise ValueError(f"Unknown AudioMode value: '{audio_mode_text}'!")

        instance = cls()
        instance.__mute = data.get("mute", False)
        instance.__is_speakers = data.get("is_speakers", True)
        instance.__speakers_audio_mode = deserialize_audio_mode(
            data.get("speakers_audio_mode", AudioMode.AM_STEREO.value))
        instance.__headphones_audio_mode = deserialize_audio_mode(
            data.get("headphones_audio_mode", AudioMode.AM_STEREO.value))
        instance.__direct_mode_enabled = data.get("direct_mode_enabled", False)
        instance.__spdif_out_direct_mode_enabled = data.get("spdif_out_direct_mode_enabled", False)
        for name, v in data.get("volumes", {}).items():
            try:
                ch = deserialize_channel(channel_text=name)
                instance.__volumes[ch] = int(v)
            except (KeyError, TypeError) as e:
                raise RuntimeError(f"Unknown channel '{name}': {e}")
        filter_str = data.get("filter")
        if filter_str:
            try:
                instance.__filter = PlaybackFilter[filter_str]
            except KeyError as e:
                raise RuntimeError(f"Unknown filter '{filter_str}': {e}")
        return instance
