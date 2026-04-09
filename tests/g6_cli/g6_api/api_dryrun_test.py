from __future__ import annotations

from collections.abc import Callable

import pytest

import g6_cli.g6_api as g6_api
from g6_cli.g6_model import Profile
from g6_cli.g6_spec import AudioFeature, PlaybackFilter, SmartVolumeSpecialHex
from g6_cli.g6_spec.decoder import DecoderMode
from g6_cli.g6_spec.recording import MicrophoneEqualizerPreset


@pytest.fixture()
def api(monkeypatch: pytest.MonkeyPatch) -> g6_api.G6Api:
    return g6_api.G6Api(dry_run=True, debug=True, persist_model=False)


# args_factory returns (args_tuple, kwargs_dict)
ArgFactory = Callable[[], tuple[tuple, dict]]

# noinspection PyListCreation
CASES: list[tuple[str, ArgFactory]] = []

# @formatter:off
# ─── Playback ───
CASES.append(("playback_mute", lambda: ((True,), {})))
CASES.append(("playback_mute", lambda: ((False,), {})))
CASES.append(("playback_toggle_to_speakers", lambda: ((), {})))
CASES.append(("playback_toggle_to_headphones", lambda: ((), {})))
CASES.append(("playback_speakers_to_stereo", lambda: ((), {})))
CASES.append(("playback_speakers_to_5_1", lambda: ((), {})))
CASES.append(("playback_speakers_to_7_1", lambda: ((), {})))
CASES.append(("playback_headphones_to_stereo", lambda: ((), {})))
CASES.append(("playback_headphones_to_5_1", lambda: ((), {})))
CASES.append(("playback_headphones_to_7_1", lambda: ((), {})))
CASES.append(("playback_volume", lambda: ((0,), {})))
CASES.append(("playback_volume", lambda: ((50,), {})))
CASES.append(("playback_volume", lambda: ((100,), {})))
CASES.append(("playback_enable_direct_mode", lambda: ((True,), {})))
CASES.append(("playback_enable_direct_mode", lambda: ((False,), {})))
CASES.append(("playback_enable_spdif_out_direct_mode", lambda: ((True,), {})))
CASES.append(("playback_enable_spdif_out_direct_mode", lambda: ((False,), {})))
for playback_filter in PlaybackFilter:
    CASES.append(("playback_filter", lambda: ((playback_filter,), {})))

# ─── Decoder ───
for decoder in DecoderMode:
    CASES.append(("decoder_mode", lambda: ((decoder,), {})))

# ─── Lighting ───
CASES.append(("lighting_disable", lambda: ((), {})))
CASES.append(("lighting_enable_set_rgb", lambda: ((), {"red": 0, "green": 0, "blue": 0})))
CASES.append(("lighting_enable_set_rgb", lambda: ((), {"red": 12, "green": 34, "blue": 56})))
CASES.append(("lighting_enable_set_rgb", lambda: ((), {"red": 255, "green": 255, "blue": 255})))

# ─── Mixer ───
CASES.append(("mixer_playback_mute", lambda: ((True,), {})))
CASES.append(("mixer_playback_mute", lambda: ((False,), {})))
CASES.append(("mixer_monitoring_line_in_mute", lambda: ((True,), {})))
CASES.append(("mixer_monitoring_line_in_mute", lambda: ((False,), {})))
CASES.append(("mixer_monitoring_line_in_volume", lambda: ((0,), {})))
CASES.append(("mixer_monitoring_line_in_volume", lambda: ((30,), {})))
CASES.append(("mixer_monitoring_line_in_volume", lambda: ((100,), {})))
CASES.append(("mixer_monitoring_external_mic_mute", lambda: ((True,), {})))
CASES.append(("mixer_monitoring_external_mic_mute", lambda: ((False,), {})))
CASES.append(("mixer_monitoring_external_mic_volume", lambda: ((0,), {})))
CASES.append(("mixer_monitoring_external_mic_volume", lambda: ((10,), {})))
CASES.append(("mixer_monitoring_external_mic_volume", lambda: ((100,), {})))
CASES.append(("mixer_monitoring_spdif_in_mute", lambda: ((True,), {})))
CASES.append(("mixer_monitoring_spdif_in_mute", lambda: ((False,), {})))
CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ((0,), {})))
CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ((80,), {})))
CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ((100,), {})))
CASES.append(("mixer_recording_line_in_mute", lambda: ((True,), {})))
CASES.append(("mixer_recording_line_in_mute", lambda: ((False,), {})))
CASES.append(("mixer_recording_line_in_volume", lambda: ((0,), {})))
CASES.append(("mixer_recording_line_in_volume", lambda: ((60,), {})))
CASES.append(("mixer_recording_line_in_volume", lambda: ((100,), {})))
CASES.append(("mixer_recording_external_mic_mute", lambda: ((True,), {})))
CASES.append(("mixer_recording_external_mic_mute", lambda: ((False,), {})))
CASES.append(("mixer_recording_external_mic_volume", lambda: ((0,), {})))
CASES.append(("mixer_recording_external_mic_volume", lambda: ((70,), {})))
CASES.append(("mixer_recording_external_mic_volume", lambda: ((100,), {})))
CASES.append(("mixer_recording_spdif_in_mute", lambda: ((True,), {})))
CASES.append(("mixer_recording_spdif_in_mute", lambda: ((False,), {})))
CASES.append(("mixer_recording_spdif_in_volume", lambda: ((0,), {})))
CASES.append(("mixer_recording_spdif_in_volume", lambda: ((10,), {})))
CASES.append(("mixer_recording_spdif_in_volume", lambda: ((100,), {})))
CASES.append(("mixer_recording_what_u_hear_mute", lambda: ((True,), {})))
CASES.append(("mixer_recording_what_u_hear_mute", lambda: ((False,), {})))
CASES.append(("mixer_recording_what_u_hear_volume", lambda: ((0,), {})))
CASES.append(("mixer_recording_what_u_hear_volume", lambda: ((40,), {})))
CASES.append(("mixer_recording_what_u_hear_volume", lambda: ((100,), {})))

# ─── Recording ───
CASES.append(("recording_mute", lambda: ((True,), {})))
CASES.append(("recording_mute", lambda: ((False,), {})))
CASES.append(("recording_mic_recording_volume", lambda: ((0,), {})))
CASES.append(("recording_mic_recording_volume", lambda: ((30,), {})))
CASES.append(("recording_mic_recording_volume", lambda: ((100,), {})))
CASES.append(("recording_mic_boost", lambda: ((0,), {})))
CASES.append(("recording_mic_monitoring_mute", lambda: ((True,), {})))
CASES.append(("recording_mic_monitoring_mute", lambda: ((False,), {})))
CASES.append(("recording_mic_monitoring_volume", lambda: ((0,), {})))
CASES.append(("recording_mic_monitoring_volume", lambda: ((70,), {})))
CASES.append(("recording_mic_monitoring_volume", lambda: ((100,), {})))
CASES.append(("recording_voice_clarity_noise_reduction_enabled", lambda: ((True,), {})))
CASES.append(("recording_voice_clarity_noise_reduction_enabled", lambda: ((False,), {})))
CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ((0,), {})))
CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ((20,), {})))
CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ((100,), {})))
CASES.append(("recording_voice_clarity_acoustic_echo_cancellation_enabled", lambda: ((True,), {})))
CASES.append(("recording_voice_clarity_acoustic_echo_cancellation_enabled", lambda: ((False,), {})))
CASES.append(("recording_voice_clarity_smart_volume_enabled", lambda: ((True,), {})))
CASES.append(("recording_voice_clarity_smart_volume_enabled", lambda: ((False,), {})))
CASES.append(("recording_voice_clarity_mic_equalizer_enabled", lambda: ((True,), {})))
CASES.append(("recording_voice_clarity_mic_equalizer_enabled", lambda: ((False,), {})))
for preset in MicrophoneEqualizerPreset:
    CASES.append(("recording_voice_clarity_mic_equalizer_preset", lambda: ((preset,), {})))

# ─── SBX ───
for audio_feature in AudioFeature:
    CASES.append(("sbx_toggle", lambda: ((), {"profile_name": Profile.Name.SPECIAL, "audio_feature": audio_feature, "activate": True})))
    CASES.append(("sbx_toggle", lambda: ((), {"profile_name": Profile.Name.SPECIAL, "audio_feature": audio_feature, "activate": False})))
for audio_feature in AudioFeature:
    CASES.append(("sbx_slider", lambda: ((), {"profile_name": Profile.Name.SPECIAL, "audio_feature": audio_feature, "value": 0})))
    CASES.append(("sbx_slider", lambda: ((), {"profile_name": Profile.Name.SPECIAL, "audio_feature": audio_feature, "value": 42})))
    CASES.append(("sbx_slider", lambda: ((), {"profile_name": Profile.Name.SPECIAL, "audio_feature": audio_feature, "value": 100})))
for smart_volume_special_hex in SmartVolumeSpecialHex:
    CASES.append(("sbx_smart_volume_special", lambda: ((), {"profile_name": Profile.Name.SPECIAL, "smart_volume_special_hex": smart_volume_special_hex})))
# @formatter:on

@pytest.mark.parametrize(
    "method_name,args_factory",
    CASES,
    ids=[f"{i}__{name}" for i, (name, _) in enumerate(CASES)])
def test_g6api_methods_execute_in_dry_run_without_errors(
        api: g6_api.G6Api,
        method_name: str,
        args_factory: ArgFactory,
) -> None:
    """
    Integration-style unit test:
    - uses the real *_spec functions
    - uses the real send_* functions
    - relies on dry_run=True to avoid hardware I/O
    """
    method = getattr(api, method_name)
    args, kwargs = args_factory()

    result = method(*args, **kwargs)

    assert result is None
