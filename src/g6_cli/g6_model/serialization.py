from g6_cli.g6_spec import Channel


class SerializationError(Exception):
    def __init__(self, cause: Exception):
        super().__init__(f"Unable to serialize model: {cause}")


class DeserializationError(Exception):
    def __init__(self, cause: Exception) -> None:
        super().__init__(f"Unable to deserialize model: {cause}")


def serialize_channel(channel: Channel) -> str:
    match channel:
        case Channel.CHANNEL_1:
            return 'left'
        case Channel.CHANNEL_2:
            return 'right'
        case _:
            raise ValueError(f"Unknown channel: {channel}")


def deserialize_channel(channel_text: str) -> Channel:
    match channel_text:
        case 'left':
            return Channel.CHANNEL_1
        case 'right':
            return Channel.CHANNEL_2
        case _:
            raise ValueError(f"Unknown channel: {channel_text}")
