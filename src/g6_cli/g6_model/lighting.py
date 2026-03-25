class Lighting:
    """Lighting audio component."""

    def __init__(self):
        self.__enabled: bool | None = None
        self.__red: int | None = None
        self.__green: int | None = None
        self.__blue: int | None = None

    @classmethod
    def default(cls):
        instance = cls()
        instance.__enabled = False
        instance.__red = 0
        instance.__green = 0
        instance.__blue = 0
        return instance

    def get_enabled(self) -> bool:
        """
        Get lighting enabled state.
        """
        return self.__enabled

    def set_enabled(self, enabled: bool) -> None:
        """
        Set lighting enabled state.
        """
        self.__enabled = enabled

    def get_rgb(self) -> tuple[int, int, int]:
        """
        Get current RGB values.
        """
        return self.__red, self.__green, self.__blue

    def set_rgb(self, red: int, green: int, blue: int) -> None:
        """
        Set RGB lighting (automatically enables lighting).
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("RGB components must be between 0 and 255")
        self.__red = red
        self.__green = green
        self.__blue = blue
        self.__enabled = True

    def to_dict(self) -> dict:
        return {
            "enabled": self.__enabled,
            "red": self.__red,
            "green": self.__green,
            "blue": self.__blue,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Lighting":
        instance = cls()
        instance.__enabled = data.get("enabled", False)
        instance.__red = data.get("red", 0)
        instance.__green = data.get("green", 0)
        instance.__blue = data.get("blue", 0)
        return instance
