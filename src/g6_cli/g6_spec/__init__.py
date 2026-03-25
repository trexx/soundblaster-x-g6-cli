from enum import Enum


class DataFragmentStatic(Enum):
    PREFIX = bytes.fromhex('5a')
    RECORDING_INTERMEDIATE = bytes.fromhex('0195')
    PLAYBACK_INTERMEDIATE = bytes.fromhex('0196')
    DECODER_INTERMEDIATE = bytes.fromhex('0197')


class DataFragmentMode(Enum):
    DATA = bytes.fromhex('1207')
    COMMIT = bytes.fromhex('1103')


class SmartVolumeSpecialHex(Enum):
    SMART_VOLUME_NIGHT = bytes.fromhex('00000040')
    SMART_VOLUME_LOUD = bytes.fromhex('0000803f')


class AudioFeature(Enum):
    SURROUND_TOGGLE = bytes.fromhex('00')
    SURROUND_SLIDER = bytes.fromhex('01')
    CRYSTALIZER_TOGGLE = bytes.fromhex('07')
    CRYSTALIZER_SLIDER = bytes.fromhex('08')
    BASS_TOGGLE = bytes.fromhex('18')
    BASS_SLIDER = bytes.fromhex('19')
    SMART_VOLUME_TOGGLE = bytes.fromhex('04')
    SMART_VOLUME_SLIDER = bytes.fromhex('05')
    SMART_VOLUME_SPECIAL = bytes.fromhex('06')
    DIALOG_PLUS_TOGGLE = bytes.fromhex('02')
    DIALOG_PLUS_SLIDER = bytes.fromhex('03')


class PlaybackFilter(Enum):
    FAST_ROLL_OFF_MINIMUM_PHASE = bytes.fromhex('0001')
    SLOW_ROLL_OFF_MINIMUM_PHASE = bytes.fromhex('0002')
    FAST_ROLL_OFF_LINEAR_PHASE = bytes.fromhex('0004')
    SLOW_ROLL_OFF_LINEAR_PHASE = bytes.fromhex('0005')


class Channel(Enum):
    CHANNEL_1 = bytes.fromhex('0102')  # LEFT
    CHANNEL_2 = bytes.fromhex('0202')  # RIGHT

    def serialize(self) -> str:
        match self:
            case Channel.CHANNEL_1:
                return 'left'
            case Channel.CHANNEL_2:
                return 'right'
            case _:
                raise ValueError(f"Unknown channel: {self}")

    @staticmethod
    def deserialize(channel_text: str) -> "Channel":
        match channel_text:
            case 'left':
                return Channel.CHANNEL_1
            case 'right':
                return Channel.CHANNEL_2
            case _:
                raise ValueError(f"Unknown channel: {channel_text}")

    def __lt__(self, other):
        """
        Makes this enum sortable for in-order channel serialization in model file ('left channel' before 'right channel').
        """
        if not isinstance(other, Channel):
            return NotImplemented
        return self.value < other.value


class UsbAudioData:
    def __init__(self, b_request: bytes, w_value: bytes, w_index: bytes, w_length: bytes, data_fragment: bytes):
        # bmRequestType
        # Data Phase Transfer Direction (bit 7): Host-to-device
        # Type (bit 6..5): Class-Request
        # Recipient (bit 4..0): Interface
        self.__bmRequestType = bytes.fromhex('21')
        self.__bRequest = b_request
        self.__wValue = w_value
        self.__wIndex = w_index
        assert len(data_fragment) == int.from_bytes(w_length, byteorder='little')
        self.__wLength = w_length
        self.__data_fragment = data_fragment

    def get_bm_request_type(self) -> bytes:
        return self.__bmRequestType

    def get_b_request(self) -> bytes:
        return self.__bRequest

    def get_w_value(self) -> bytes:
        return self.__wValue

    def get_w_index(self) -> bytes:
        return self.__wIndex

    def get_w_length(self) -> bytes:
        return self.__wLength

    def get_data_fragment(self) -> bytes:
        return self.__data_fragment


EMPTY_ADDITIONAL_PAYLOAD = bytes.fromhex(''.zfill(108))


class UsbHidDataFragment:
    def __init__(self, mode: bytes, audio_feature: bytes, intermediate: bytes, value: bytes, additional_payload: bytes):
        self.__static_prefix = DataFragmentStatic.PREFIX.value
        self.__mode = mode
        self.__static_intermediate = intermediate
        self.__audio_feature = audio_feature
        self.__value = value
        self.__additional_payload = additional_payload

    @classmethod
    def from_enum(cls, mode: DataFragmentMode, audio_feature: AudioFeature, value: bytes):
        return cls(mode=mode.value, audio_feature=audio_feature.value,
                   intermediate=DataFragmentStatic.PLAYBACK_INTERMEDIATE.value, value=value,
                   additional_payload=EMPTY_ADDITIONAL_PAYLOAD)

    @classmethod
    def being_data(cls, audio_feature: bytes, value: bytes):
        return cls(mode=DataFragmentMode.DATA.value, audio_feature=audio_feature,
                   intermediate=DataFragmentStatic.PLAYBACK_INTERMEDIATE.value, value=value,
                   additional_payload=EMPTY_ADDITIONAL_PAYLOAD)

    @classmethod
    def being_commit(cls, audio_feature: bytes, value: bytes):
        return cls(mode=DataFragmentMode.COMMIT.value, audio_feature=audio_feature,
                   intermediate=DataFragmentStatic.PLAYBACK_INTERMEDIATE.value, value=value,
                   additional_payload=EMPTY_ADDITIONAL_PAYLOAD)

    @classmethod
    def empty_additional_payload(cls, mode: bytes, audio_feature: bytes, intermediate: bytes, value: bytes):
        return cls(mode=mode, audio_feature=audio_feature, intermediate=intermediate, value=value,
                   additional_payload=EMPTY_ADDITIONAL_PAYLOAD)

    def __str__(self):
        hex_value = self.__to_hex()
        if not len(hex_value) == 128:
            raise ValueError(f'Generated hex-line string has unexpected length \'{len(hex_value)}\'! '
                             f'Expected length is 128, but was \'{hex_value}\'!')
        return hex_value

    def __repr__(self):
        return self.__to_hex()

    def __to_hex(self):
        return (f'{self.__static_prefix.hex()}{self.__mode.hex()}{self.__static_intermediate.hex()}'
                f'{self.__audio_feature.hex()}{self.__value.hex()}{self.__additional_payload.hex()}')


class ValueRange:
    def __init__(self, min_value, step_size, max_value):
        self.__min_value = min_value
        self.__step_size = step_size
        self.__max_value = max_value

    def get_min_value(self):
        return self.__min_value

    def get_step_size(self):
        return self.__step_size

    def get_max_value(self):
        return self.__max_value


# ─── Global values ───

B_REQUEST = bytes.fromhex('01')

BOTH_CHANNELS = {Channel.CHANNEL_1, Channel.CHANNEL_2}

# ─── Playback ───

PLAYBACK_PLAYBACK = bytes.fromhex('0001')

# ─── Mixer ───

MONITORING_LINE_IN = bytes.fromhex('0009')
MONITORING_EXTERNAL_MIC: bytes = bytes.fromhex('000A')
MONITORING_SPDIF_IN = bytes.fromhex('000C')

# ─── Recording ───

RECORDING_LINE_IN = bytes.fromhex('0003')
RECORDING_EXTERNAL_MIC = bytes.fromhex('0004')
RECORDING_SPDIF_IN = bytes.fromhex('0005')
RECORDING_WHAT_U_HEAR = bytes.fromhex('0006')

# -- Volumes and Decibels --

__slider_percent_to_bytes_dict: dict[int, bytes] = {
    0: bytes.fromhex('0000 0000'),
    1: bytes.fromhex('0ad7 233c'),
    2: bytes.fromhex('0ad7 a33c'),
    3: bytes.fromhex('8fc2 f53c'),
    4: bytes.fromhex('0ad7 233d'),
    5: bytes.fromhex('cdcc 4c3d'),
    6: bytes.fromhex('8fc2 753d'),
    7: bytes.fromhex('295c 8f3d'),
    8: bytes.fromhex('0ad7 a33d'),
    9: bytes.fromhex('ec51 b83d'),
    10: bytes.fromhex('cdcc cc3d'),
    11: bytes.fromhex('ae47 e13d'),
    12: bytes.fromhex('8fc2 f53d'),
    13: bytes.fromhex('b81e 053e'),
    14: bytes.fromhex('295c 0f3e'),
    15: bytes.fromhex('9a99 193e'),
    16: bytes.fromhex('0ad7 233e'),
    17: bytes.fromhex('7b14 2e3e'),
    18: bytes.fromhex('ec51 383e'),
    19: bytes.fromhex('5c8f 423e'),
    20: bytes.fromhex('cdcc 4c3e'),
    21: bytes.fromhex('3d0a 573e'),
    22: bytes.fromhex('ae47 613e'),
    23: bytes.fromhex('1f85 6b3e'),
    24: bytes.fromhex('8fc2 753e'),
    25: bytes.fromhex('0000 803e'),
    26: bytes.fromhex('b81e 853e'),
    27: bytes.fromhex('713d 8a3e'),
    28: bytes.fromhex('295c 8f3e'),
    29: bytes.fromhex('e17a 943e'),
    30: bytes.fromhex('9a99 993e'),
    31: bytes.fromhex('52b8 9e3e'),
    32: bytes.fromhex('0ad7 a33e'),
    33: bytes.fromhex('c3f5 a83e'),
    34: bytes.fromhex('7b14 ae3e'),
    35: bytes.fromhex('3333 b33e'),
    36: bytes.fromhex('ec51 b83e'),
    37: bytes.fromhex('a470 bd3e'),
    38: bytes.fromhex('5c8f c23e'),
    39: bytes.fromhex('14ae c73e'),
    40: bytes.fromhex('cdcc cc3e'),
    41: bytes.fromhex('85eb d13e'),
    42: bytes.fromhex('3d0a d73e'),
    43: bytes.fromhex('f628 dc3e'),
    44: bytes.fromhex('ae47 e13e'),
    45: bytes.fromhex('6666 e63e'),
    46: bytes.fromhex('1f85 eb3e'),
    47: bytes.fromhex('d7a3 f03e'),
    48: bytes.fromhex('8fc2 f53e'),
    49: bytes.fromhex('48e1 fa3e'),
    50: bytes.fromhex('0000 003f'),
    51: bytes.fromhex('5c8f 023f'),
    52: bytes.fromhex('b81e 053f'),
    53: bytes.fromhex('14ae 073f'),
    54: bytes.fromhex('713d 0a3f'),
    55: bytes.fromhex('cdcc 0c3f'),
    56: bytes.fromhex('295c 0f3f'),
    57: bytes.fromhex('85eb 113f'),
    58: bytes.fromhex('e17a 143f'),
    59: bytes.fromhex('3d0a 173f'),
    60: bytes.fromhex('9a99 193f'),
    61: bytes.fromhex('f628 1c3f'),
    62: bytes.fromhex('52b8 1e3f'),
    63: bytes.fromhex('ae47 213f'),
    64: bytes.fromhex('0ad7 233f'),
    65: bytes.fromhex('6666 263f'),
    66: bytes.fromhex('c3f5 283f'),
    67: bytes.fromhex('1f85 2b3f'),
    68: bytes.fromhex('7b14 2e3f'),
    69: bytes.fromhex('d7a3 303f'),
    70: bytes.fromhex('3333 333f'),
    71: bytes.fromhex('8fc2 353f'),
    72: bytes.fromhex('ec51 383f'),
    73: bytes.fromhex('48e1 3a3f'),
    74: bytes.fromhex('a470 3d3f'),
    75: bytes.fromhex('0000 403f'),
    76: bytes.fromhex('5c8f 423f'),
    77: bytes.fromhex('b81e 453f'),
    78: bytes.fromhex('14ae 473f'),
    79: bytes.fromhex('713d 4a3f'),
    80: bytes.fromhex('cdcc 4c3f'),
    81: bytes.fromhex('295c 4f3f'),
    82: bytes.fromhex('85eb 513f'),
    83: bytes.fromhex('e17a 543f'),
    84: bytes.fromhex('3d0a 573f'),
    85: bytes.fromhex('9a99 593f'),
    86: bytes.fromhex('f628 5c3f'),
    87: bytes.fromhex('52b8 5e3f'),
    88: bytes.fromhex('ae47 613f'),
    89: bytes.fromhex('0ad7 633f'),
    90: bytes.fromhex('6666 663f'),
    91: bytes.fromhex('c3f5 683f'),
    92: bytes.fromhex('1f85 6b3f'),
    93: bytes.fromhex('7b14 6e3f'),
    94: bytes.fromhex('d7a3 703f'),
    95: bytes.fromhex('3333 733f'),
    96: bytes.fromhex('8fc2 753f'),
    97: bytes.fromhex('ec51 783f'),
    98: bytes.fromhex('48e1 7a3f'),
    99: bytes.fromhex('a470 7d3f'),
    100: bytes.fromhex('0000 803f'),
}

__playback_volume_percent_to_bytes_dict: dict[int, bytes] = {
    0: bytes.fromhex('00c0'),
    10: bytes.fromhex('e7de'),
    20: bytes.fromhex('69e8'),
    30: bytes.fromhex('37ee'),
    40: bytes.fromhex('68f2'),
    50: bytes.fromhex('b0f5'),
    60: bytes.fromhex('62f8'),
    70: bytes.fromhex('acfa'),
    80: bytes.fromhex('aafc'),
    90: bytes.fromhex('6cfe'),
    100: bytes.fromhex('0000'),
}

__mic_recording_volume_percent_to_bytes_dict: dict[int, bytes] = {
    0: bytes.fromhex('00d0'),
    10: bytes.fromhex('2ee6'),
    20: bytes.fromhex('d7ee'),
    30: bytes.fromhex('52f4'),
    40: bytes.fromhex('57f8'),
    50: bytes.fromhex('84fb'),
    60: bytes.fromhex('25fe'),
    70: bytes.fromhex('6400'),
    80: bytes.fromhex('c202'),
    90: bytes.fromhex('8f05'),
    100: bytes.fromhex('0009'),
}

__mic_monitoring_volume_percent_to_bytes_dict: dict[int, bytes] = __playback_volume_percent_to_bytes_dict

__mic_boost_decibel_to_bytes_dict: dict[int, bytes] = {
    0: bytes.fromhex('0000 0000'),
    10: bytes.fromhex('0a00 0000'),
    20: bytes.fromhex('1400 0000'),
    30: bytes.fromhex('1e00 0000')
}

__mic_voice_clarity_level_to_bytes_dict: dict[int, bytes] = {
    0: bytes.fromhex('0000 0000'),
    20: bytes.fromhex('cdcc cc3d'),
    40: bytes.fromhex('cdcc 4c3e'),
    60: bytes.fromhex('9a99 993e'),
    80: bytes.fromhex('cdcc cc3e'),
    100: bytes.fromhex('0000 003f')
}


def get_slider_percent_bytes(percent_value: int) -> bytes:
    return __slider_percent_to_bytes_dict[percent_value]


def get_playback_volume_percent_bytes(percent_value: int) -> bytes:
    return __playback_volume_percent_to_bytes_dict[percent_value]


def get_mic_recording_volume_percent_bytes(percent_value: int) -> bytes:
    return __mic_recording_volume_percent_to_bytes_dict[percent_value]


def get_mic_monitoring_volume_percent_bytes(percent_value: int) -> bytes:
    return __mic_monitoring_volume_percent_to_bytes_dict[percent_value]


def get_mic_boost_decibel_bytes(decibel: int) -> bytes:
    return __mic_boost_decibel_to_bytes_dict[decibel]


def get_mic_voice_clarity_level_bytes(level: int) -> bytes:
    return __mic_voice_clarity_level_to_bytes_dict[level]
