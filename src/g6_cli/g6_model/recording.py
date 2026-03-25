from g6_cli.g6_model.serialization import deserialize_channel, serialize_channel
from g6_cli.g6_spec import Channel, BOTH_CHANNELS
from g6_cli.g6_spec.recording import MicrophoneEqualizerPreset


class Recording:
    """Recording audio component."""

    def __init__(self):
        self.__mute: bool | None = None
        self.__mic_recording_volumes: dict[Channel, int] | None = None
        self.__mic_boost: int | None = None
        self.__mic_monitoring_mute: bool | None = None
        self.__mic_monitoring_volumes: dict[Channel, int] | None = None
        self.__voice_clarity_enabled: bool | None = None
        self.__voice_clarity_noise_reduction_level: int | None = None
        self.__voice_clarity_acoustic_echo_cancellation_enabled: bool | None = None
        self.__voice_clarity_smart_volume_enabled: bool | None = None
        self.__voice_clarity_mic_equalizer_enabled: bool | None = None
        self.__voice_clarity_mic_equalizer_preset: MicrophoneEqualizerPreset | None = None

    @classmethod
    def default(cls):
        instance = cls()
        instance.__mute = False
        instance.__mic_recording_volumes = {channel: 50 for channel in BOTH_CHANNELS}
        instance.__mic_boost = 0
        instance.__mic_monitoring_mute = False
        instance.__mic_monitoring_volumes = {channel: 50 for channel in BOTH_CHANNELS}
        instance.__voice_clarity_enabled = False
        instance.__voice_clarity_noise_reduction_level = 0
        instance.__voice_clarity_acoustic_echo_cancellation_enabled = False
        instance.__voice_clarity_smart_volume_enabled = False
        instance.__voice_clarity_mic_equalizer_enabled = False
        instance.__voice_clarity_mic_equalizer_preset = list(MicrophoneEqualizerPreset)[0]
        return instance

    @staticmethod
    def __validate_mic_recording_volume(volume_percent: int) -> None:
        if volume_percent < 0 or volume_percent > 100 or volume_percent % 10 != 0:
            raise ValueError(f"Mic recording volume must be 0-100 in steps of 10, got {volume_percent}")

    @staticmethod
    def __validate_mic_boost(decibel: int) -> None:
        if decibel < 0 or decibel > 30 or decibel % 10 != 0:
            raise ValueError(f"Mic boost must be 0-30 dB in steps of 10, got {decibel}")

    @staticmethod
    def __validate_voice_clarity_noise_reduction_level(level_percent: int) -> None:
        if level_percent < 0 or level_percent > 100 or level_percent % 20 != 0:
            raise ValueError(f"Voice clarity level must be 0-100 in steps of 20, got {level_percent}")

    def get_mute(self) -> bool:
        """
        Get recording mute state.
        """
        return self.__mute

    def set_mute(self, mute: bool) -> None:
        """
        Set recording mute state.
        """
        self.__mute = mute

    def get_mic_recording_volume(self, channel: Channel) -> int:
        """
        Get mic recording volume for channel.
        """
        return self.__mic_recording_volumes.get(channel, 50)

    def set_mic_recording_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        """
        Set mic recording volume.
        """
        self.__validate_mic_recording_volume(volume_percent)
        for ch in channels:
            if ch in self.__mic_recording_volumes:
                self.__mic_recording_volumes[ch] = volume_percent

    def get_mic_boost(self) -> int:
        """
        Get mic boost level (dB).
        """
        return self.__mic_boost

    def set_mic_boost(self, decibel: int) -> None:
        """
        Set mic boost level.
        """
        self.__validate_mic_boost(decibel)
        self.__mic_boost = decibel

    def get_mic_monitoring_mute(self) -> bool:
        """
        Get mic monitoring mute state.
        """
        return self.__mic_monitoring_mute

    def set_mic_monitoring_mute(self, mute: bool) -> None:
        """
        Set mic monitoring mute state.
        """
        self.__mic_monitoring_mute = mute

    def get_mic_monitoring_volume(self, channel: Channel) -> int:
        """
        Get mic monitoring volume for channel.
        """
        return self.__mic_monitoring_volumes.get(channel, 50)

    def set_mic_monitoring_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        """
        Set mic monitoring volume.
        """
        self.__validate_mic_recording_volume(volume_percent)  # same range/step as recording volume
        for ch in channels:
            if ch in self.__mic_monitoring_volumes:
                self.__mic_monitoring_volumes[ch] = volume_percent

    def get_voice_clarity_enabled(self) -> bool:
        """
        Get voice clarity enabled state.
        """
        return self.__voice_clarity_enabled

    def set_voice_clarity_enabled(self, enable: bool) -> None:
        """
        Set voice clarity enabled state.
        """
        self.__voice_clarity_enabled = enable

    def get_voice_clarity_noise_reduction_level(self) -> int:
        """
        Get voice clarity noise reduction level.
        """
        return self.__voice_clarity_noise_reduction_level

    def set_voice_clarity_noise_reduction_level(self, level_percent: int) -> None:
        """
        Set voice clarity noise reduction level.
        """
        self.__validate_voice_clarity_noise_reduction_level(level_percent)
        self.__voice_clarity_noise_reduction_level = level_percent

    def get_voice_clarity_acoustic_echo_cancellation_enabled(self) -> bool:
        """
        Get acoustic echo cancellation enabled state.
        """
        return self.__voice_clarity_acoustic_echo_cancellation_enabled

    def set_voice_clarity_acoustic_echo_cancellation_enabled(self, enable: bool) -> None:
        """
        Set acoustic echo cancellation enabled state.
        """
        self.__voice_clarity_acoustic_echo_cancellation_enabled = enable

    def get_voice_clarity_smart_volume_enabled(self) -> bool:
        """
        Get smart volume enabled state.
        """
        return self.__voice_clarity_smart_volume_enabled

    def set_voice_clarity_smart_volume_enabled(self, enable: bool) -> None:
        """
        Set smart volume enabled state.
        """
        self.__voice_clarity_smart_volume_enabled = enable

    def get_voice_clarity_mic_equalizer_enabled(self) -> bool:
        """
        Get mic equalizer enabled state.
        """
        return self.__voice_clarity_mic_equalizer_enabled

    def set_voice_clarity_mic_equalizer_enabled(self, enable: bool) -> None:
        """
        Set mic equalizer enabled state.
        """
        self.__voice_clarity_mic_equalizer_enabled = enable

    def get_voice_clarity_mic_equalizer_preset(self) -> MicrophoneEqualizerPreset:
        """
        Get mic equalizer preset.
        """
        return self.__voice_clarity_mic_equalizer_preset

    def set_voice_clarity_mic_equalizer_preset(self, preset: MicrophoneEqualizerPreset) -> None:
        """
        Set mic equalizer preset.
        """
        if not isinstance(preset, MicrophoneEqualizerPreset):
            raise ValueError(f"preset must be MicrophoneEqualizerPreset, got {type(preset)}")
        self.__voice_clarity_mic_equalizer_preset = preset

    def to_dict(self) -> dict:
        return {
            "mute": self.__mute,
            "mic_recording_volumes": {serialize_channel(channel=ch): v for ch, v in
                                      sorted(self.__mic_recording_volumes.items())},
            "mic_boost": self.__mic_boost,
            "mic_monitoring_mute": self.__mic_monitoring_mute,
            "mic_monitoring_volumes": {serialize_channel(channel=ch): v for ch, v in
                                       sorted(self.__mic_monitoring_volumes.items())},
            "voice_clarity_enabled": self.__voice_clarity_enabled,
            "voice_clarity_noise_reduction_level": self.__voice_clarity_noise_reduction_level,
            "voice_clarity_acoustic_echo_cancellation_enabled": self.__voice_clarity_acoustic_echo_cancellation_enabled,
            "voice_clarity_smart_volume_enabled": self.__voice_clarity_smart_volume_enabled,
            "voice_clarity_mic_equalizer_enabled": self.__voice_clarity_mic_equalizer_enabled,
            "voice_clarity_mic_equalizer_preset": self.__voice_clarity_mic_equalizer_preset.name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Recording":
        instance = cls()
        instance.__mute = data.get("mute", False)
        instance.__mic_boost = data.get("mic_boost", 0)
        instance.__mic_monitoring_mute = data.get("mic_monitoring_mute", False)
        instance.__voice_clarity_enabled = data.get("voice_clarity_enabled", False)
        instance.__voice_clarity_noise_reduction_level = data.get("voice_clarity_noise_reduction_level", 0)
        instance.__voice_clarity_acoustic_echo_cancellation_enabled = data.get(
            "voice_clarity_acoustic_echo_cancellation_enabled", False
        )
        instance.__voice_clarity_smart_volume_enabled = data.get("voice_clarity_smart_volume_enabled", False)
        instance.__voice_clarity_mic_equalizer_enabled = data.get("voice_clarity_mic_equalizer_enabled", False)

        instance.__mic_recording_volumes = {}
        for name, v in data.get("mic_recording_volumes", {}).items():
            try:
                ch = deserialize_channel(channel_text=name)
                instance.__mic_recording_volumes[ch] = int(v)
            except (KeyError, TypeError) as e:
                raise RuntimeError(f"Unknown channel '{name}': {e}")

        instance.__mic_monitoring_volumes = {}
        for name, v in data.get("mic_monitoring_volumes", {}).items():
            try:
                ch = deserialize_channel(channel_text=name)
                instance.__mic_monitoring_volumes[ch] = int(v)
            except (KeyError, TypeError) as e:
                raise RuntimeError(f"Unknown channel '{name}': {e}")

        preset_str = data.get("voice_clarity_mic_equalizer_preset")
        if preset_str:
            try:
                instance.__voice_clarity_mic_equalizer_preset = MicrophoneEqualizerPreset[preset_str]
            except KeyError as e:
                raise RuntimeError(f"Unknown preset_str '{preset_str}': {e}")
        return instance
