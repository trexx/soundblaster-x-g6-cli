from g6_cli.g6_spec import SmartVolumeSpecialHex


class SBXFeature:
    """
    Base class for SBX audio features that support toggle and/or slider control.
    """

    def __init__(
            self,
            name: str,
            toggle_value: bool,
            slider_value: int
    ):
        self.__name = name
        self.__toggle_value: bool = toggle_value
        self.__slider_value: int = slider_value

    def get_toggle(self) -> bool:
        return self.__toggle_value

    def set_toggle(self, activate: bool) -> None:
        self.__toggle_value = activate

    def get_slider(self) -> int:
        return self.__slider_value

    def set_slider(self, value: int) -> None:
        if value < 0 or value > 100:
            raise ValueError(f"Slider value must be between 0 and 100, got {value}")
        self.__slider_value = value

    def to_dict(self) -> dict:
        return {"name": self.__name, "toggle_value": str(self.__toggle_value).lower(),
                "slider_value": str(self.__slider_value)}

    @classmethod
    def from_dict(cls, data: dict) -> "SBXFeature":
        name = data.get("name")
        toggle_value: bool = data.get("toggle_value") == 'true'
        slider_value: int = int(data.get("slider_value"))
        return cls(name=name, toggle_value=toggle_value, slider_value=slider_value)

    def __str__(self):
        return f"name='{self.__name,}', toggle_value={self.__toggle_value}, slider_value={self.__slider_value}"

    def __repr__(self) -> str:
        return self.__str__()


class SmartVolumeSBXFeature(SBXFeature):

    def __init__(self, name: str, toggle_value: bool, slider_value: int, special_value: SmartVolumeSpecialHex | None):
        super().__init__(name=name, toggle_value=toggle_value, slider_value=slider_value)
        self.__special_value = special_value

    def get_special_value(self) -> SmartVolumeSpecialHex:
        return self.__special_value

    def set_special_value(self, value: SmartVolumeSpecialHex) -> None:
        self.__special_value = value

    def to_dict(self) -> dict:
        _dict = super().to_dict()
        # add special_value to dict
        special_value_text: str
        match self.__special_value:
            case SmartVolumeSpecialHex.SMART_VOLUME_NIGHT:
                special_value_text = 'Night'
            case SmartVolumeSpecialHex.SMART_VOLUME_LOUD:
                special_value_text = 'Loud'
            case _:
                special_value_text = 'None'
        _dict["special_value"] = special_value_text
        return _dict

    def __str__(self):
        return f"{super().__str__()}, special_value={self.__special_value}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, data: dict) -> "SmartVolumeSBXFeature":
        name = data.get("name")
        toggle_value = data.get("toggle_value") == 'true'
        slider_value = int(data.get("slider_value"))
        special_value_text = data.get("special_value")
        special_value: SmartVolumeSpecialHex | None
        match special_value_text:
            case 'Night':
                special_value = SmartVolumeSpecialHex.SMART_VOLUME_NIGHT
            case 'Loud':
                special_value = SmartVolumeSpecialHex.SMART_VOLUME_LOUD
            case _:
                special_value = None
        return cls(name=name, toggle_value=toggle_value, slider_value=slider_value, special_value=special_value)


class SBX:
    """SBX audio component with typed feature instances."""

    def __init__(self):
        self.__surround = SBXFeature(
            name="Surround",
            toggle_value=False,
            slider_value=50
        )
        self.__crystalizer = SBXFeature(
            name="Crystalizer",
            toggle_value=False,
            slider_value=50
        )
        self.__bass = SBXFeature(
            name="Bass",
            toggle_value=False,
            slider_value=50
        )
        self.__smart_volume = SmartVolumeSBXFeature(
            name="Smart Volume",
            toggle_value=False,
            slider_value=50,
            special_value=None
        )
        self.__dialog_plus = SBXFeature(
            name="Dialog Plus",
            toggle_value=False,
            slider_value=50
        )

    # ── Surround ────────────────────────────────────────────────────────────────

    def get_surround_toggle(self) -> bool:
        return self.__surround.get_toggle()

    def set_surround_toggle(self, activate: bool) -> None:
        self.__surround.set_toggle(activate)

    def get_surround_slider(self) -> int:
        return self.__surround.get_slider()

    def set_surround_slider(self, value: int) -> None:
        self.__surround.set_slider(value)

    # ── Crystalizer ─────────────────────────────────────────────────────────────
    def get_crystalizer_toggle(self) -> bool:
        return self.__crystalizer.get_toggle()

    def set_crystalizer_toggle(self, activate: bool) -> None:
        self.__crystalizer.set_toggle(activate)

    def get_crystalizer_slider(self) -> int:
        return self.__crystalizer.get_slider()

    def set_crystalizer_slider(self, value: int) -> None:
        self.__crystalizer.set_slider(value)

    # ── Bass ────────────────────────────────────────────────────────────────────
    def get_bass_toggle(self) -> bool:
        return self.__bass.get_toggle()

    def set_bass_toggle(self, activate: bool) -> None:
        self.__bass.set_toggle(activate)

    def get_bass_slider(self) -> int:
        return self.__bass.get_slider()

    def set_bass_slider(self, value: int) -> None:
        self.__bass.set_slider(value)

    # ── Smart Volume ────────────────────────────────────────────────────────────
    def get_smart_volume_toggle(self) -> bool:
        return self.__smart_volume.get_toggle()

    def set_smart_volume_toggle(self, activate: bool) -> None:
        self.__smart_volume.set_toggle(activate)

    def get_smart_volume_slider(self) -> int:
        return self.__smart_volume.get_slider()

    def set_smart_volume_slider(self, value: int) -> None:
        self.__smart_volume.set_slider(value)

    def get_smart_volume_special(self) -> SmartVolumeSpecialHex:
        return self.__smart_volume.get_special_value()

    def set_smart_volume_special(self, value: SmartVolumeSpecialHex) -> None:
        self.__smart_volume.set_special_value(value=value)

    # ── Dialog Plus ─────────────────────────────────────────────────────────────
    def get_dialog_plus_toggle(self) -> bool:
        return self.__dialog_plus.get_toggle()

    def set_dialog_plus_toggle(self, activate: bool) -> None:
        self.__dialog_plus.set_toggle(activate)

    def get_dialog_plus_slider(self) -> int:
        return self.__dialog_plus.get_slider()

    def set_dialog_plus_slider(self, value: int) -> None:
        self.__dialog_plus.set_slider(value)

    ## ──────────────────────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "surround": self.__surround.to_dict(),
            "crystalizer": self.__crystalizer.to_dict(),
            "bass": self.__bass.to_dict(),
            "smart_volume": self.__smart_volume.to_dict(),
            "dialog_plus": self.__dialog_plus.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SBX":
        instance = cls()
        instance.__surround = SBXFeature.from_dict(data["surround"])
        instance.__crystalizer = SBXFeature.from_dict(data["crystalizer"])
        instance.__bass = SBXFeature.from_dict(data["bass"])
        instance.__smart_volume = SmartVolumeSBXFeature.from_dict(data["smart_volume"])
        instance.__dialog_plus = SBXFeature.from_dict(data["dialog_plus"])
        return instance
