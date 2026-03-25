from __future__ import annotations

from collections.abc import Callable
from unittest.mock import MagicMock

import pytest

import g6_cli.g6_api as g6_api
from g6_cli.g6_core import G6Device
from g6_cli.g6_spec import AudioFeature, Channel
from g6_cli.g6_model import Profile


@pytest.fixture()
def api(monkeypatch: pytest.MonkeyPatch) -> g6_api.G6Api:
    """
    Always construct with dry_run=True (per requirement) and never touch real hardware.
    """
    # mock detect_device() method on g6_api module level
    monkeypatch.setattr(g6_api, "detect_device", MagicMock(return_value=G6Device))
    return g6_api.G6Api(dry_run=True, debug=True, persist_model=False)


# args_factory returns (args_tuple, kwargs_dict)
ArgFactory = Callable[[], tuple[tuple, dict]]

# noinspection PyListCreation
NEGATIVE_AUDIO_CASES: list[tuple[str, str, ArgFactory, str]] = []

# @formatter:off
# ─── Playback (audio) ───
NEGATIVE_AUDIO_CASES.append(("playback_volume", "playback_volume_spec", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("playback_volume", "playback_volume_spec", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("playback_volume", "playback_volume_spec", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

# ─── Mixer (audio) ───
NEGATIVE_AUDIO_CASES.append(("mixer_monitoring_line_in_volume", "monitoring_line_in_volume_spec", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("mixer_monitoring_line_in_volume", "monitoring_line_in_volume_spec", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("mixer_monitoring_line_in_volume", "monitoring_line_in_volume_spec", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_AUDIO_CASES.append(("mixer_monitoring_external_mic_volume", "monitoring_external_mic_volume_spec", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("mixer_monitoring_external_mic_volume", "monitoring_external_mic_volume_spec", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("mixer_monitoring_external_mic_volume", "monitoring_external_mic_volume_spec", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_AUDIO_CASES.append(("mixer_monitoring_spdif_in_volume", "monitoring_spdif_in_volume_spec", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("mixer_monitoring_spdif_in_volume", "monitoring_spdif_in_volume_spec", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("mixer_monitoring_spdif_in_volume", "monitoring_spdif_in_volume_spec", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_AUDIO_CASES.append(("mixer_recording_line_in_volume", "recording_line_in_volume_spec", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("mixer_recording_line_in_volume", "recording_line_in_volume_spec", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("mixer_recording_line_in_volume", "recording_line_in_volume_spec", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_AUDIO_CASES.append(("mixer_recording_external_mic_volume", "recording_external_mic_volume_spec", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("mixer_recording_external_mic_volume", "recording_external_mic_volume_spec", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("mixer_recording_external_mic_volume", "recording_external_mic_volume_spec", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_AUDIO_CASES.append(("mixer_recording_spdif_in_volume", "recording_spdif_in_volume_spec", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("mixer_recording_spdif_in_volume", "recording_spdif_in_volume_spec", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("mixer_recording_spdif_in_volume", "recording_spdif_in_volume_spec", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_AUDIO_CASES.append(("mixer_recording_what_u_hear_volume", "recording_what_u_hear_volume_spec", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("mixer_recording_what_u_hear_volume", "recording_what_u_hear_volume_spec", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("mixer_recording_what_u_hear_volume", "recording_what_u_hear_volume_spec", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

# ─── Recording (audio) ───
NEGATIVE_AUDIO_CASES.append(("recording_mic_recording_volume", "mic_recording_volume_spec", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("recording_mic_recording_volume", "mic_recording_volume_spec", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("recording_mic_recording_volume", "mic_recording_volume_spec", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_AUDIO_CASES.append(("recording_mic_boost", "mic_boost_spec", lambda: ((), {"decibel": -10}), "between 0 and 30 dB, got -10"))
NEGATIVE_AUDIO_CASES.append(("recording_mic_boost", "mic_boost_spec", lambda: ((), {"decibel": 40}), "between 0 and 30 dB, got 40"))
NEGATIVE_AUDIO_CASES.append(("recording_mic_boost", "mic_boost_spec", lambda: ((), {"decibel": 15}), "multiple of 10 dB, got 15"))

NEGATIVE_AUDIO_CASES.append(("recording_mic_monitoring_volume", "mic_monitoring_volume_spec", lambda: ((), {"volume_percent": -1, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("recording_mic_monitoring_volume", "mic_monitoring_volume_spec", lambda: ((), {"volume_percent": 101, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("recording_mic_monitoring_volume", "mic_monitoring_volume_spec", lambda: ((), {"volume_percent": 5, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}}), "multiple of 10, got 5"))

NEGATIVE_AUDIO_CASES.append(("recording_voice_clarity_noise_reduction_level", "voice_clarity_noise_reduction_level_spec", lambda: ((), {"level_percent": -1}), "between 0 and 100, got -1"))
NEGATIVE_AUDIO_CASES.append(("recording_voice_clarity_noise_reduction_level", "voice_clarity_noise_reduction_level_spec", lambda: ((), {"level_percent": 101}), "between 0 and 100, got 101"))
NEGATIVE_AUDIO_CASES.append(("recording_voice_clarity_noise_reduction_level", "voice_clarity_noise_reduction_level_spec", lambda: ((), {"level_percent": 10}), "multiple of 20, got 10"))
# @formatter:on

# noinspection PyListCreation
NEGATIVE_HID_CASES: list[tuple[str, str, ArgFactory, str]] = []

# @formatter:off
# ─── Lighting (hid) ───
NEGATIVE_HID_CASES.append(("lighting_enable_set_rgb", "lighting_enable_set_rgb_spec", lambda: ((), {"red": -1, "green": 0, "blue": 0}), "red must be between 0 and 255, got -1"))
NEGATIVE_HID_CASES.append(("lighting_enable_set_rgb", "lighting_enable_set_rgb_spec", lambda: ((), {"red": 256, "green": 0, "blue": 0}), "red must be between 0 and 255, got 256"))
NEGATIVE_HID_CASES.append(("lighting_enable_set_rgb", "lighting_enable_set_rgb_spec", lambda: ((), {"red": 0, "green": -1, "blue": 0}), "green must be between 0 and 255, got -1"))
NEGATIVE_HID_CASES.append(("lighting_enable_set_rgb", "lighting_enable_set_rgb_spec", lambda: ((), {"red": 0, "green": 256, "blue": 0}), "green must be between 0 and 255, got 256"))
NEGATIVE_HID_CASES.append(("lighting_enable_set_rgb", "lighting_enable_set_rgb_spec", lambda: ((), {"red": 0, "green": 0, "blue": -1}), "blue must be between 0 and 255, got -1"))
NEGATIVE_HID_CASES.append(("lighting_enable_set_rgb", "lighting_enable_set_rgb_spec", lambda: ((), {"red": 0, "green": 0, "blue": 256}), "blue must be between 0 and 255, got 256"))

# ─── SBX (hid) ───
NEGATIVE_HID_CASES.append(("sbx_slider", "sbx_slider_spec", lambda: ((), {"profile_name": Profile.Name.SPECIAL, "audio_feature": AudioFeature.SURROUND_SLIDER, "value": -1}), "between 0 and 100, got -1"))
NEGATIVE_HID_CASES.append(("sbx_slider", "sbx_slider_spec", lambda: ((), {"profile_name": Profile.Name.SPECIAL, "audio_feature": AudioFeature.SURROUND_SLIDER, "value": 101}), "between 0 and 100, got 101"))
# @formatter:on


@pytest.mark.parametrize(
    "method_name,spec_name,args_factory,expected_error_snippet",
    NEGATIVE_AUDIO_CASES,
    ids=[f"{i}__{method_name}" for i, (method_name, _, _, _) in enumerate(NEGATIVE_AUDIO_CASES)],
)
def test_g6api_audio_methods_raise_on_invalid_args(
        api: g6_api.G6Api,
        monkeypatch: pytest.MonkeyPatch,
        method_name: str,
        spec_name: str,
        args_factory: ArgFactory,
        expected_error_snippet: str,
) -> None:
    args, kwargs = args_factory()

    # Patch the sender to assert not called
    device = getattr(api, "_G6Api__device")
    send_mock = MagicMock()
    monkeypatch.setattr(device, "send_audio_data_to_device", send_mock)

    with pytest.raises(ValueError) as exc_info:
        method = getattr(api, method_name)
        method(*args, **kwargs)

    assert expected_error_snippet in str(exc_info.value)
    send_mock.assert_not_called()


@pytest.mark.parametrize(
    "method_name,spec_name,args_factory,expected_error_snippet",
    NEGATIVE_HID_CASES,
    ids=[f"{i}__{method_name}" for i, (method_name, _, _, _) in enumerate(NEGATIVE_HID_CASES)],
)
def test_g6api_hid_methods_raise_on_invalid_args(
        api: g6_api.G6Api,
        monkeypatch: pytest.MonkeyPatch,
        method_name: str,
        spec_name: str,
        args_factory: ArgFactory,
        expected_error_snippet: str,
) -> None:
    args, kwargs = args_factory()

    # Patch the sender to assert not called
    device = getattr(api, "_G6Api__device")
    send_mock = MagicMock()
    monkeypatch.setattr(device, "send_hid_data_to_device", send_mock)

    with pytest.raises(ValueError) as exc_info:
        method = getattr(api, method_name)
        method(*args, **kwargs)

    assert expected_error_snippet in str(exc_info.value)
    send_mock.assert_not_called()
