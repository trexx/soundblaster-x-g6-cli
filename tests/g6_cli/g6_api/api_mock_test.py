from __future__ import annotations

from collections.abc import Callable
from typing import Any
from unittest.mock import MagicMock

import pytest

import g6_cli.g6_api as g6_api
from g6_cli.g6_core import G6Device
from g6_cli.g6_model import Profile
from g6_cli.g6_spec import AudioFeature, PlaybackFilter, SmartVolumeSpecialHex, Channel
from g6_cli.g6_spec.decoder import DecoderMode
from g6_cli.g6_spec.recording import MicrophoneEqualizerPreset


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
AUDIO_CASES: list[tuple[str, str, ArgFactory]] = []

# @formatter:off
# ─── Playback (audio) ───
AUDIO_CASES.append(("playback_mute", "playback_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("playback_mute", "playback_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("playback_speakers_to_stereo", "speakers_to_stereo_spec", lambda: ((), {})))
AUDIO_CASES.append(("playback_speakers_to_5_1", "speakers_to_5_1_spec", lambda: ((), {})))
AUDIO_CASES.append(("playback_speakers_to_7_1", "speakers_to_7_1_spec", lambda: ((), {})))
AUDIO_CASES.append(("playback_headphones_to_stereo", "headphones_to_stereo_spec", lambda: ((), {})))
AUDIO_CASES.append(("playback_headphones_to_5_1", "headphones_to_5_1_spec", lambda: ((), {})))
AUDIO_CASES.append(("playback_headphones_to_7_1", "headphones_to_7_1_spec", lambda: ((), {})))
AUDIO_CASES.append(("playback_volume", "playback_volume_spec", lambda: ((), {"volume_percent": 0, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("playback_volume", "playback_volume_spec", lambda: ((), {"volume_percent": 50, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("playback_volume", "playback_volume_spec", lambda: ((), {"volume_percent": 100, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))

# ─── Mixer (audio) ───
AUDIO_CASES.append(("mixer_playback_mute", "mixer_playback_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("mixer_playback_mute", "mixer_playback_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("mixer_monitoring_line_in_mute", "monitoring_line_in_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("mixer_monitoring_line_in_mute", "monitoring_line_in_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("mixer_monitoring_line_in_volume", "monitoring_line_in_volume_spec", lambda: ((), {"volume_percent": 0, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_monitoring_line_in_volume", "monitoring_line_in_volume_spec", lambda: ((), {"volume_percent": 30, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_monitoring_line_in_volume", "monitoring_line_in_volume_spec", lambda: ((), {"volume_percent": 100, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_monitoring_external_mic_mute", "monitoring_external_mic_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("mixer_monitoring_external_mic_mute", "monitoring_external_mic_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("mixer_monitoring_external_mic_volume", "monitoring_external_mic_volume_spec", lambda: ((), {"volume_percent": 0, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_monitoring_external_mic_volume", "monitoring_external_mic_volume_spec", lambda: ((), {"volume_percent": 10, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_monitoring_external_mic_volume", "monitoring_external_mic_volume_spec", lambda: ((), {"volume_percent": 100, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_monitoring_spdif_in_mute", "monitoring_spdif_in_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("mixer_monitoring_spdif_in_mute", "monitoring_spdif_in_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("mixer_monitoring_spdif_in_volume", "monitoring_spdif_in_volume_spec", lambda: ((), {"volume_percent": 0, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_monitoring_spdif_in_volume", "monitoring_spdif_in_volume_spec", lambda: ((), {"volume_percent": 80, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_monitoring_spdif_in_volume", "monitoring_spdif_in_volume_spec", lambda: ((), {"volume_percent": 100, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_line_in_mute", "recording_line_in_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("mixer_recording_line_in_mute", "recording_line_in_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("mixer_recording_line_in_volume", "recording_line_in_volume_spec", lambda: ((), {"volume_percent": 0, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_line_in_volume", "recording_line_in_volume_spec", lambda: ((), {"volume_percent": 60, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_line_in_volume", "recording_line_in_volume_spec", lambda: ((), {"volume_percent": 100, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_external_mic_mute", "recording_external_mic_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("mixer_recording_external_mic_mute", "recording_external_mic_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("mixer_recording_external_mic_volume", "recording_external_mic_volume_spec", lambda: ((), {"volume_percent": 0, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_external_mic_volume", "recording_external_mic_volume_spec", lambda: ((), {"volume_percent": 70, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_external_mic_volume", "recording_external_mic_volume_spec", lambda: ((), {"volume_percent": 100, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_spdif_in_mute", "recording_spdif_in_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("mixer_recording_spdif_in_mute", "recording_spdif_in_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("mixer_recording_spdif_in_volume", "recording_spdif_in_volume_spec", lambda: ((), {"volume_percent": 0, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_spdif_in_volume", "recording_spdif_in_volume_spec", lambda: ((), {"volume_percent": 10, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_spdif_in_volume", "recording_spdif_in_volume_spec", lambda: ((), {"volume_percent": 100, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_what_u_hear_mute", "recording_what_u_hear_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("mixer_recording_what_u_hear_mute", "recording_what_u_hear_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("mixer_recording_what_u_hear_volume", "recording_what_u_hear_volume_spec", lambda: ((), {"volume_percent": 0, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_what_u_hear_volume", "recording_what_u_hear_volume_spec", lambda: ((), {"volume_percent": 40, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("mixer_recording_what_u_hear_volume", "recording_what_u_hear_volume_spec", lambda: ((), {"volume_percent": 100, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))

# ─── Recording (audio) ───
AUDIO_CASES.append(("recording_mute", "recording_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("recording_mute", "recording_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("recording_mic_recording_volume", "mic_recording_volume_spec", lambda: ((), {"volume_percent": 0, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("recording_mic_recording_volume", "mic_recording_volume_spec", lambda: ((), {"volume_percent": 30, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("recording_mic_recording_volume", "mic_recording_volume_spec", lambda: ((), {"volume_percent": 100, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("recording_mic_monitoring_mute", "mic_monitoring_mute_spec", lambda: ((), {"mute": True})))
AUDIO_CASES.append(("recording_mic_monitoring_mute", "mic_monitoring_mute_spec", lambda: ((), {"mute": False})))
AUDIO_CASES.append(("recording_mic_monitoring_volume", "mic_monitoring_volume_spec", lambda: ((), {"volume_percent": 0, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("recording_mic_monitoring_volume", "mic_monitoring_volume_spec", lambda: ((), {"volume_percent": 60, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))
AUDIO_CASES.append(("recording_mic_monitoring_volume", "mic_monitoring_volume_spec", lambda: ((), {"volume_percent": 100, "channels": {Channel.CHANNEL_1, Channel.CHANNEL_2}})))

# noinspection PyListCreation
HID_CASES: list[tuple[str, str, ArgFactory]] = []

# ─── Playback (hid) ───
HID_CASES.append(("playback_toggle_to_speakers", "toggle_to_speakers_spec", lambda: ((), {})))
HID_CASES.append(("playback_toggle_to_headphones", "toggle_to_headphones_spec", lambda: ((), {})))
HID_CASES.append(("playback_enable_direct_mode", "enable_direct_mode_spec", lambda: ((), {"enable": True})))
HID_CASES.append(("playback_enable_direct_mode", "enable_direct_mode_spec", lambda: ((), {"enable": False})))
HID_CASES.append(("playback_enable_spdif_out_direct_mode", "enable_spdif_out_direct_mode_spec", lambda: ((), {"enable": True})))
HID_CASES.append(("playback_enable_spdif_out_direct_mode", "enable_spdif_out_direct_mode_spec", lambda: ((), {"enable": False})))
for playback_filter in PlaybackFilter:
    HID_CASES.append(("playback_filter", "playback_filter_spec", lambda pf=playback_filter: ((), {"playback_filter_enum": pf})))

# ─── Decoder (hid) ───
for decoder in DecoderMode:
    HID_CASES.append(("decoder_mode", "decoder_mode_spec", lambda d=decoder: ((), {"decoder_mode_enum": d})))

# ─── Lighting (hid) ───
HID_CASES.append(("lighting_disable", "lighting_disable_spec", lambda: ((), {})))
HID_CASES.append(("lighting_enable_set_rgb", "lighting_enable_set_rgb_spec", lambda: ((), {"red": 0, "green": 0, "blue": 0})))
HID_CASES.append(("lighting_enable_set_rgb", "lighting_enable_set_rgb_spec", lambda: ((), {"red": 12, "green": 34, "blue": 56})))
HID_CASES.append(("lighting_enable_set_rgb", "lighting_enable_set_rgb_spec", lambda: ((), {"red": 255, "green": 255, "blue": 255})))

# ─── Recording (hid) ───
HID_CASES.append(("recording_mic_boost", "mic_boost_spec", lambda: ((), {"decibel": 0})))
HID_CASES.append(("recording_mic_boost", "mic_boost_spec", lambda: ((), {"decibel": 10})))
HID_CASES.append(("recording_voice_clarity_enabled", "voice_clarity_enabled_spec", lambda: ((), {"enable": True})))
HID_CASES.append(("recording_voice_clarity_enabled", "voice_clarity_enabled_spec", lambda: ((), {"enable": False})))
HID_CASES.append(("recording_voice_clarity_noise_reduction_level", "voice_clarity_noise_reduction_level_spec", lambda: ((), {"level_percent": 0})))
HID_CASES.append(("recording_voice_clarity_noise_reduction_level", "voice_clarity_noise_reduction_level_spec", lambda: ((), {"level_percent": 20})))
HID_CASES.append(("recording_voice_clarity_noise_reduction_level", "voice_clarity_noise_reduction_level_spec", lambda: ((), {"level_percent": 100})))
HID_CASES.append(("recording_voice_clarity_acoustic_echo_cancellation_enabled", "voice_clarity_acoustic_echo_cancellation_enabled_spec", lambda: ((), {"enable": True})))
HID_CASES.append(("recording_voice_clarity_acoustic_echo_cancellation_enabled", "voice_clarity_acoustic_echo_cancellation_enabled_spec", lambda: ((), {"enable": False})))
HID_CASES.append(("recording_voice_clarity_smart_volume_enabled", "voice_clarity_smart_volume_enabled_spec", lambda: ((), {"enable": True})))
HID_CASES.append(("recording_voice_clarity_smart_volume_enabled", "voice_clarity_smart_volume_enabled_spec", lambda: ((), {"enable": False})))
HID_CASES.append(("recording_voice_clarity_mic_equalizer_enabled", "voice_clarity_mic_equalizer_enabled_spec", lambda: ((), {"enable": True})))
HID_CASES.append(("recording_voice_clarity_mic_equalizer_enabled", "voice_clarity_mic_equalizer_enabled_spec", lambda: ((), {"enable": False})))
for preset in MicrophoneEqualizerPreset:
    HID_CASES.append(("recording_voice_clarity_mic_equalizer_preset", "voice_clarity_mic_equalizer_preset_spec", lambda p=preset: ((), {"preset": p})))

# ─── SBX (hid) ───
for audio_feature in AudioFeature:
    HID_CASES.append(("sbx_toggle", "sbx_toggle_spec", lambda af=audio_feature: ((), {"audio_feature": af, "activate": True})))
    HID_CASES.append(("sbx_toggle", "sbx_toggle_spec", lambda af=audio_feature: ((), {"audio_feature": af, "activate": False})))
for audio_feature in AudioFeature:
    HID_CASES.append(("sbx_slider", "sbx_slider_spec", lambda af=audio_feature: ((), {"audio_feature": af, "value": 0})))
    HID_CASES.append(("sbx_slider", "sbx_slider_spec", lambda af=audio_feature: ((), {"audio_feature": af, "value": 40})))
    HID_CASES.append(("sbx_slider", "sbx_slider_spec", lambda af=audio_feature: ((), {"audio_feature": af, "value": 100})))
for smart_volume_special_hex in SmartVolumeSpecialHex:
    HID_CASES.append(("sbx_smart_volume_special","sbx_smart_volume_special_spec", lambda sv=smart_volume_special_hex: ((), {"smart_volume_special_hex": sv}),))
# @formatter:on


@pytest.mark.parametrize(
    "method_name,spec_name,args_factory",
    AUDIO_CASES,
    ids=[f"{i}__{method_name}" for i, (method_name, _, _) in enumerate(AUDIO_CASES)],
)
def test_g6api_audio_methods_call_audio_sender(
        api: g6_api.G6Api,
        monkeypatch: pytest.MonkeyPatch,
        method_name: str,
        spec_name: str,
        args_factory: ArgFactory,
) -> None:
    args, kwargs = args_factory()

    # Create a mock for hex data ("*_spec()" method in g6_api)
    expected_audio_data_list = [b"audio-payload"]
    spec_mock = MagicMock(return_value=expected_audio_data_list)
    monkeypatch.setattr(g6_api, spec_name, spec_mock)

    # Patch the instance method: api.__device.send_audio_data_to_device(...)
    device = getattr(api, "_G6Api__device")
    send_audio_mock = MagicMock()
    monkeypatch.setattr(device, "send_audio_data_to_device", send_audio_mock)

    # Execute method on g6_api instance
    method = getattr(api, method_name)
    method(*args, **kwargs)

    # Assert: correct spec method called
    spec_mock.assert_called_once_with(*args, **kwargs)

    # Assert: send_audio_data_to_device called correctly
    send_audio_mock.assert_called_once_with(audio_data_list=expected_audio_data_list)


@pytest.mark.parametrize(
    "method_name,spec_name,args_factory",
    HID_CASES,
    ids=[f"{i}__{method_name}" for i, (method_name, _, _) in enumerate(HID_CASES)],
)
def test_g6api_hid_methods_call_hid_sender(
        api: g6_api.G6Api,
        monkeypatch: pytest.MonkeyPatch,
        method_name: str,
        spec_name: str,
        args_factory: ArgFactory,
) -> None:
    args, kwargs = args_factory()

    # Prepare kwargs to use test method invocation
    method_kwargs: dict[str, Any]
    if method_name in ("sbx_toggle", "sbx_slider", "sbx_smart_volume_special"):
        method_kwargs = kwargs.copy()
        method_kwargs.update({"profile_name": Profile.Name.SPECIAL})
    else:
        method_kwargs = kwargs
    spec_kwargs = kwargs

    # Create a mock for hex data ("*_spec()" method in g6_api)
    expected_hid_data_list = [b"hid-payload"]
    spec_mock = MagicMock(return_value=expected_hid_data_list)
    monkeypatch.setattr(g6_api, spec_name, spec_mock)

    # Patch the instance method: api.__device.send_hid_data_to_device(...)
    device = getattr(api, "_G6Api__device")
    send_hid_mock = MagicMock()
    monkeypatch.setattr(device, "send_hid_data_to_device", send_hid_mock)

    # Execute method on g6_api instance
    method = getattr(api, method_name)
    method(**method_kwargs)

    # Assert: correct spec method called
    spec_mock.assert_called_once_with(**spec_kwargs)

    # Assert: send_hid_data_to_device called correctly
    send_hid_mock.assert_called_once_with(hid_data_list=expected_hid_data_list)
