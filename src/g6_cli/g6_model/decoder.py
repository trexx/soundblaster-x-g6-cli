from g6_cli.g6_spec.decoder import DecoderMode


class Decoder:
    """Decoder audio component."""

    def __init__(self):
        self.__mode: DecoderMode | None = None

    @classmethod
    def default(cls):
        instance = cls()
        instance.__mode = DecoderMode.NORMAL
        return instance

    def get_mode(self) -> DecoderMode:
        """
        Get the decoder mode.
        """
        return self.__mode

    def set_mode(self, mode: DecoderMode) -> None:
        """
        Set the decoder mode.
        """
        if not isinstance(mode, DecoderMode):
            raise ValueError(f"mode must be DecoderMode, got {type(mode)}")
        self.__mode = mode

    def to_dict(self) -> dict:
        return {"mode": self.__mode.name}

    @classmethod
    def from_dict(cls, data: dict) -> "Decoder":
        instance = cls()
        mode_str = data.get("mode")
        if mode_str:
            try:
                instance.__mode = DecoderMode[mode_str]
            except KeyError as e:
                raise RuntimeError(f"Invalid decoder mode '{mode_str}': {e}")
        return instance
