from g6_cli.g6_model.serialization import serialize_channel, deserialize_channel
from g6_cli.g6_spec import Channel, BOTH_CHANNELS


class Mixer:
    """Mixer audio component."""

    def __init__(self):
        self.__playback_mute: bool = False
        self.__monitoring_line_in_mute: bool = False
        self.__monitoring_line_in_volumes: dict[Channel, int] = {channel: 50 for channel in BOTH_CHANNELS}
        self.__monitoring_external_mic_mute: bool = False
        self.__monitoring_external_mic_volumes: dict[Channel, int] = {channel: 50 for channel in BOTH_CHANNELS}
        self.__monitoring_spdif_in_mute: bool = False
        self.__monitoring_spdif_in_volumes: dict[Channel, int] = {channel: 50 for channel in BOTH_CHANNELS}
        self.__recording_line_in_mute: bool = False
        self.__recording_line_in_volumes: dict[Channel, int] = {channel: 50 for channel in BOTH_CHANNELS}
        self.__recording_external_mic_mute: bool = False
        self.__recording_external_mic_volumes: dict[Channel, int] = {channel: 50 for channel in BOTH_CHANNELS}
        self.__recording_spdif_in_mute: bool = False
        self.__recording_spdif_in_volumes: dict[Channel, int] = {channel: 50 for channel in BOTH_CHANNELS}
        self.__recording_what_u_hear_mute: bool = False
        self.__recording_what_u_hear_volumes: dict[Channel, int] = {channel: 50 for channel in BOTH_CHANNELS}

    @staticmethod
    def __validate_volume_percent(volume_percent: int) -> None:
        if volume_percent < 0 or volume_percent > 100:
            raise ValueError(f"Volume percentage must be between 0 and 100, got {volume_percent}")
        if volume_percent % 10 != 0:
            raise ValueError(f"Volume percentage must be a multiple of 10, got {volume_percent}")

    def get_playback_mute(self) -> bool:
        """
        Get mixer playback mute state.
        """
        return self.__playback_mute

    def set_playback_mute(self, mute: bool) -> None:
        """
        Set mixer playback mute state.
        """
        self.__playback_mute = mute

    def get_monitoring_line_in_mute(self) -> bool:
        """
        Get monitoring Line-In mute state.
        """
        return self.__monitoring_line_in_mute

    def set_monitoring_line_in_mute(self, mute: bool) -> None:
        """
        Set monitoring Line-In mute state.
        """
        self.__monitoring_line_in_mute = mute

    def get_monitoring_line_in_volume(self, channel: Channel) -> int:
        """
        Get monitoring Line-In volume for channel.
        """
        return self.__monitoring_line_in_volumes.get(channel, 50)

    def set_monitoring_line_in_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        """
        Set monitoring Line-In volume.
        """
        self.__validate_volume_percent(volume_percent)
        for ch in channels:
            if ch in self.__monitoring_line_in_volumes:
                self.__monitoring_line_in_volumes[ch] = volume_percent

    # (identical pattern repeated for all other monitoring/recording units - abbreviated for brevity but fully implemented in the real file)
    def get_monitoring_external_mic_mute(self) -> bool:
        return self.__monitoring_external_mic_mute

    def set_monitoring_external_mic_mute(self, mute: bool) -> None:
        self.__monitoring_external_mic_mute = mute

    def get_monitoring_external_mic_volume(self, channel: Channel) -> int:
        return self.__monitoring_external_mic_volumes.get(channel, 50)

    def set_monitoring_external_mic_volume(self, volume_percent: int,
                                           channels: set[Channel] = BOTH_CHANNELS) -> None:
        self.__validate_volume_percent(volume_percent)
        for ch in channels:
            if ch in self.__monitoring_external_mic_volumes:
                self.__monitoring_external_mic_volumes[ch] = volume_percent

    def get_monitoring_spdif_in_mute(self) -> bool:
        return self.__monitoring_spdif_in_mute

    def set_monitoring_spdif_in_mute(self, mute: bool) -> None:
        self.__monitoring_spdif_in_mute = mute

    def get_monitoring_spdif_in_volume(self, channel: Channel) -> int:
        return self.__monitoring_spdif_in_volumes.get(channel, 50)

    def set_monitoring_spdif_in_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        self.__validate_volume_percent(volume_percent)
        for ch in channels:
            if ch in self.__monitoring_spdif_in_volumes:
                self.__monitoring_spdif_in_volumes[ch] = volume_percent

    def get_recording_line_in_mute(self) -> bool:
        return self.__recording_line_in_mute

    def set_recording_line_in_mute(self, mute: bool) -> None:
        self.__recording_line_in_mute = mute

    def get_recording_line_in_volume(self, channel: Channel) -> int:
        return self.__recording_line_in_volumes.get(channel, 50)

    def set_recording_line_in_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        self.__validate_volume_percent(volume_percent)
        for ch in channels:
            if ch in self.__recording_line_in_volumes:
                self.__recording_line_in_volumes[ch] = volume_percent

    def get_recording_external_mic_mute(self) -> bool:
        return self.__recording_external_mic_mute

    def set_recording_external_mic_mute(self, mute: bool) -> None:
        self.__recording_external_mic_mute = mute

    def get_recording_external_mic_volume(self, channel: Channel) -> int:
        return self.__recording_external_mic_volumes.get(channel, 50)

    def set_recording_external_mic_volume(self, volume_percent: int,
                                          channels: set[Channel] = BOTH_CHANNELS) -> None:
        self.__validate_volume_percent(volume_percent)
        for ch in channels:
            if ch in self.__recording_external_mic_volumes:
                self.__recording_external_mic_volumes[ch] = volume_percent

    def get_recording_spdif_in_mute(self) -> bool:
        return self.__recording_spdif_in_mute

    def set_recording_spdif_in_mute(self, mute: bool) -> None:
        self.__recording_spdif_in_mute = mute

    def get_recording_spdif_in_volume(self, channel: Channel) -> int:
        return self.__recording_spdif_in_volumes.get(channel, 50)

    def set_recording_spdif_in_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        self.__validate_volume_percent(volume_percent)
        for ch in channels:
            if ch in self.__recording_spdif_in_volumes:
                self.__recording_spdif_in_volumes[ch] = volume_percent

    def get_recording_what_u_hear_mute(self) -> bool:
        return self.__recording_what_u_hear_mute

    def set_recording_what_u_hear_mute(self, mute: bool) -> None:
        self.__recording_what_u_hear_mute = mute

    def get_recording_what_u_hear_volume(self, channel: Channel) -> int:
        return self.__recording_what_u_hear_volumes.get(channel, 50)

    def set_recording_what_u_hear_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        self.__validate_volume_percent(volume_percent)
        for ch in channels:
            if ch in self.__recording_what_u_hear_volumes:
                self.__recording_what_u_hear_volumes[ch] = volume_percent

    def to_dict(self) -> dict:
        return {
            "playback_mute": self.__playback_mute,
            "monitoring_line_in_mute": self.__monitoring_line_in_mute,
            "monitoring_line_in_volumes": {serialize_channel(channel=ch): v for ch, v in
                                           sorted(self.__monitoring_line_in_volumes.items())},
            "monitoring_external_mic_mute": self.__monitoring_external_mic_mute,
            "monitoring_external_mic_volumes": {serialize_channel(channel=ch): v for ch, v in
                                                sorted(self.__monitoring_external_mic_volumes.items())},
            "monitoring_spdif_in_mute": self.__monitoring_spdif_in_mute,
            "monitoring_spdif_in_volumes": {serialize_channel(channel=ch): v for ch, v in
                                            sorted(self.__monitoring_spdif_in_volumes.items())},
            "recording_line_in_mute": self.__recording_line_in_mute,
            "recording_line_in_volumes": {serialize_channel(channel=ch): v for ch, v in
                                          sorted(self.__recording_line_in_volumes.items())},
            "recording_external_mic_mute": self.__recording_external_mic_mute,
            "recording_external_mic_volumes": {serialize_channel(channel=ch): v for ch, v in
                                               sorted(self.__recording_external_mic_volumes.items())},
            "recording_spdif_in_mute": self.__recording_spdif_in_mute,
            "recording_spdif_in_volumes": {serialize_channel(channel=ch): v for ch, v in
                                           sorted(self.__recording_spdif_in_volumes.items())},
            "recording_what_u_hear_mute": self.__recording_what_u_hear_mute,
            "recording_what_u_hear_volumes": {serialize_channel(channel=ch): v for ch, v in
                                              sorted(self.__recording_what_u_hear_volumes.items())},
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Mixer":
        instance = cls()
        for field in (
                "playback_mute",
                "monitoring_line_in_mute",
                "monitoring_external_mic_mute",
                "monitoring_spdif_in_mute",
                "recording_line_in_mute",
                "recording_external_mic_mute",
                "recording_spdif_in_mute",
                "recording_what_u_hear_mute",
        ):
            setattr(instance, f"_{cls.__name__}__{field}", data.get(field, False))
        for vol_key, vol_dict in (
                ("monitoring_line_in_volumes", instance.__monitoring_line_in_volumes),
                ("monitoring_external_mic_volumes", instance.__monitoring_external_mic_volumes),
                ("monitoring_spdif_in_volumes", instance.__monitoring_spdif_in_volumes),
                ("recording_line_in_volumes", instance.__recording_line_in_volumes),
                ("recording_external_mic_volumes", instance.__recording_external_mic_volumes),
                ("recording_spdif_in_volumes", instance.__recording_spdif_in_volumes),
                ("recording_what_u_hear_volumes", instance.__recording_what_u_hear_volumes),
        ):
            for name, v in data.get(vol_key, {}).items():
                try:
                    ch = deserialize_channel(channel_text=name)
                    vol_dict[ch] = int(v)
                except (KeyError, TypeError) as e:
                    raise RuntimeError(f"Unknown channel '{name}': {e}")
        return instance
