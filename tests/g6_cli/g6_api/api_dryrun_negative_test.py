from __future__ import annotations

from collections.abc import Callable

import pytest

import g6_cli.g6_api as g6_api
from g6_cli.g6_model import Profile
from g6_cli.g6_spec import AudioFeature, Channel


@pytest.fixture()
def api() -> g6_api.G6Api:
    return g6_api.G6Api(dry_run=True, debug=True, persist_model=False)


# args_factory returns (args_tuple, kwargs_dict)
ArgFactory = Callable[[], tuple[tuple, dict]]

# noinspection PyListCreation
NEGATIVE_CASES: list[tuple[str, ArgFactory, str]] = []

# @formatter:off
# ─── Playback ───
NEGATIVE_CASES.append(("playback_volume", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("playback_volume", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("playback_volume", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

# ─── Mixer ───
NEGATIVE_CASES.append(("mixer_monitoring_line_in_volume", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("mixer_monitoring_line_in_volume", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("mixer_monitoring_line_in_volume", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_CASES.append(("mixer_monitoring_external_mic_volume", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("mixer_monitoring_external_mic_volume", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("mixer_monitoring_external_mic_volume", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_CASES.append(("mixer_recording_line_in_volume", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("mixer_recording_line_in_volume", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("mixer_recording_line_in_volume", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_CASES.append(("mixer_recording_external_mic_volume", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("mixer_recording_external_mic_volume", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("mixer_recording_external_mic_volume", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_CASES.append(("mixer_recording_spdif_in_volume", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("mixer_recording_spdif_in_volume", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("mixer_recording_spdif_in_volume", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_CASES.append(("mixer_recording_what_u_hear_volume", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("mixer_recording_what_u_hear_volume", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("mixer_recording_what_u_hear_volume", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

# ─── Recording ───
NEGATIVE_CASES.append(("recording_mic_recording_volume", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("recording_mic_recording_volume", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("recording_mic_recording_volume", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_CASES.append(("recording_mic_boost", lambda: ((), {"decibel": -10}), "between 0 and 30 dB, got -10"))
NEGATIVE_CASES.append(("recording_mic_boost", lambda: ((), {"decibel": 40}), "between 0 and 30 dB, got 40"))
NEGATIVE_CASES.append(("recording_mic_boost", lambda: ((), {"decibel": 15}), "multiple of 10 dB, got 15"))

NEGATIVE_CASES.append(("recording_mic_monitoring_volume", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("recording_mic_monitoring_volume", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("recording_mic_monitoring_volume", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ((), {"level_percent": -1}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ((), {"level_percent": 101}), "between 0 and 100, got 101"))
NEGATIVE_CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ((), {"level_percent": 10}), "multiple of 20, got 10"))

# ─── Lighting ───
NEGATIVE_CASES.append(("lighting_enable_set_rgb", lambda: ((), {"red": -1, "green": 0, "blue": 0}), "red must be between 0 and 255, got -1"))
NEGATIVE_CASES.append(("lighting_enable_set_rgb", lambda: ((), {"red": 256, "green": 0, "blue": 0}), "red must be between 0 and 255, got 256"))
NEGATIVE_CASES.append(("lighting_enable_set_rgb", lambda: ((), {"red": 0, "green": -1, "blue": 0}), "green must be between 0 and 255, got -1"))
NEGATIVE_CASES.append(("lighting_enable_set_rgb", lambda: ((), {"red": 0, "green": 256, "blue": 0}), "green must be between 0 and 255, got 256"))
NEGATIVE_CASES.append(("lighting_enable_set_rgb", lambda: ((), {"red": 0, "green": 0, "blue": -1}), "blue must be between 0 and 255, got -1"))
NEGATIVE_CASES.append(("lighting_enable_set_rgb", lambda: ((), {"red": 0, "green": 0, "blue": 256}), "blue must be between 0 and 255, got 256"))

# ─── SBX ───
NEGATIVE_CASES.append(("sbx_slider", lambda: ((), {"profile_name": Profile.Name.SPECIAL, "audio_feature": AudioFeature.SURROUND_SLIDER, "value": -1}), "between 0 and 100, got -1"))
NEGATIVE_CASES.append(("sbx_slider", lambda: ((), {"profile_name": Profile.Name.SPECIAL, "audio_feature": AudioFeature.SURROUND_SLIDER, "value": 101}), "between 0 and 100, got 101"))
# @formatter:on


@pytest.mark.parametrize(
    "method_name,args_factory,expected_error_snippet",
    NEGATIVE_CASES,
    ids=[f"{i}__{method_name}" for i, (method_name, _, _) in enumerate(NEGATIVE_CASES)]
)
def test_g6api_methods_raise_on_invalid_args_in_dry_run(
        api: g6_api.G6Api,
        method_name: str,
        args_factory: ArgFactory,
        expected_error_snippet: str,
) -> None:
    """
    Integration-style unit test for invalid arguments:
    - uses the real *_spec functions (which perform validation)
    - relies on dry_run=True to avoid hardware I/O
    - expects ValueError to be raised before any send attempt
    """
    args, kwargs = args_factory()

    with pytest.raises(ValueError) as exc_info:
        method = getattr(api, method_name)
        method(*args, **kwargs)

    assert expected_error_snippet in str(exc_info.value)
