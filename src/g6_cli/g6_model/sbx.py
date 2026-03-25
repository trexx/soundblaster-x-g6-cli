from enum import Enum

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
        self.__surround: SBXFeature | None = None
        self.__crystalizer: SBXFeature | None = None
        self.__bass: SBXFeature | None = None
        self.__smart_volume: SmartVolumeSBXFeature | None = None
        self.__dialog_plus: SBXFeature | None = None

    @classmethod
    def default(cls):
        instance = cls()
        instance.__surround = SBXFeature(
            name="Surround",
            toggle_value=False,
            slider_value=50
        )
        instance.__crystalizer = SBXFeature(
            name="Crystalizer",
            toggle_value=False,
            slider_value=50
        )
        instance.__bass = SBXFeature(
            name="Bass",
            toggle_value=False,
            slider_value=50
        )
        instance.__smart_volume = SmartVolumeSBXFeature(
            name="Smart Volume",
            toggle_value=False,
            slider_value=50,
            special_value=None
        )
        instance.__dialog_plus = SBXFeature(
            name="Dialog Plus",
            toggle_value=False,
            slider_value=50
        )
        return instance

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


class Profile:
    class Name(Enum):
        GAMING = "gaming"
        MUSIC = "music"
        CINEMA = "cinema"
        SPECIAL = "special"

        def serialize(self) -> str:
            return self.value

        @staticmethod
        def deserialize(value: str) -> "Profile.Name":
            for profile_name in Profile.Name:
                if profile_name.value == value:
                    return profile_name
            raise ValueError(f"No profile with name '{value}' exists!")

    def __init__(self):
        self.__profile_name: Profile.Name | None = None
        self.__sbx: SBX | None = None

    @classmethod
    def init(cls, profile_name: Name) -> "Profile":
        instance = cls()
        instance.__profile_name = profile_name
        instance.__sbx = SBX.default()
        return instance

    def get_sbx(self) -> SBX:
        return self.__sbx

    def to_dict(self):
        return {
            "profile_name": self.__profile_name.value,
            "sbx": self.__sbx.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Profile":
        instance = cls()
        instance.__profile_name = Profile.Name.deserialize(data["profile_name"])
        instance.__sbx = SBX.from_dict(data.get("sbx", {}))
        return instance


class Profiles:
    def __init__(self) -> None:
        self.__selected_profile: Profile.Name | None = None
        self.__profiles: dict[Profile.Name, Profile] | None = None

    @classmethod
    def default(cls) -> "Profiles":
        instance = cls()
        instance.__selected_profile = Profile.Name.GAMING
        instance.__profiles = {
            Profile.Name.GAMING: Profile.init(Profile.Name.GAMING),
            Profile.Name.MUSIC: Profile.init(Profile.Name.MUSIC),
            Profile.Name.CINEMA: Profile.init(Profile.Name.CINEMA),
            Profile.Name.SPECIAL: Profile.init(Profile.Name.SPECIAL),
        }
        return instance

    def get_sbx(self):
        return self.__profiles.get(self.__selected_profile).get_sbx()

    def to_dict(self) -> dict:
        return {
            "selected_profile": self.__selected_profile.serialize(),
            "profiles": {
                Profile.Name.GAMING.serialize(): self.__profiles.get(Profile.Name.GAMING).to_dict(),
                Profile.Name.MUSIC.serialize(): self.__profiles.get(Profile.Name.MUSIC).to_dict(),
                Profile.Name.CINEMA.serialize(): self.__profiles.get(Profile.Name.CINEMA).to_dict(),
                Profile.Name.SPECIAL.serialize(): self.__profiles.get(Profile.Name.SPECIAL).to_dict(),
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Profiles":
        instance = cls()

        # deserialize
        instance.__selected_profile = Profile.Name.deserialize(data["selected_profile"])
        instance.__profiles = {}
        for profile_name_value in data["profiles"]:
            instance.__profiles[Profile.Name.deserialize(profile_name_value)] = Profile.from_dict(
                data["profiles"][profile_name_value])

        # validate profiles count
        expected_profile_count = len(Profile.Name)
        actual_profile_count = len(instance.__profiles)
        if expected_profile_count != actual_profile_count:
            raise RuntimeError(
                f"An error occurred deserializing the profiles. Expected {expected_profile_count} profiles, but got {actual_profile_count} profiles!")

        return instance
