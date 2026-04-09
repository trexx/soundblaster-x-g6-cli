from __future__ import annotations

from collections.abc import Callable

import pytest

from g6_cli import main as cli_main
from g6_cli.g6_spec import PlaybackFilter
from g6_cli.g6_spec.recording import MicrophoneEqualizerPreset

# args_list returns list of CLI argument strings
ArgsListFactory = Callable[[], list[str]]

# noinspection PyListCreation
CLI_CASES: list[tuple[str, ArgsListFactory]] = []

# @formatter:off
# ─── Device / services ───
CLI_CASES.append(("reload_audio", lambda: ["--reload-audio-services"]))

# ─── Playback ───
CLI_CASES.append(("playback_toggle_to_speakers", lambda: ["--set-output", "Speakers"]))
CLI_CASES.append(("playback_toggle_to_headphones", lambda: ["--set-output", "Headphones"]))
CLI_CASES.append(("playback_toggle_to_speakers", lambda: ["--toggle-output"]))
CLI_CASES.append(("playback_mute", lambda: ["--playback-mute", "Enabled"]))
CLI_CASES.append(("playback_mute", lambda: ["--playback-mute", "Disabled"]))
CLI_CASES.append(("playback_volume", lambda: ["--playback-volume", "0"]))
CLI_CASES.append(("playback_volume", lambda: ["--playback-volume", "50"]))
CLI_CASES.append(("playback_volume", lambda: ["--playback-volume", "100"]))
CLI_CASES.append(("playback_volume", lambda: ["--playback-volume", "50", "--playback-volume-channels", "Left"]))
CLI_CASES.append(("playback_volume", lambda: ["--playback-volume", "50", "--playback-volume-channels", "Right"]))
CLI_CASES.append(("playback_speakers_to_stereo", lambda: ["--playback-speakers-to-stereo"]))
CLI_CASES.append(("playback_speakers_to_5_1", lambda: ["--playback-speakers-to-5-1"]))
CLI_CASES.append(("playback_speakers_to_7_1", lambda: ["--playback-speakers-to-7-1"]))
CLI_CASES.append(("playback_headphones_to_stereo", lambda: ["--playback-headphones-to-stereo"]))
CLI_CASES.append(("playback_headphones_to_5_1", lambda: ["--playback-headphones-to-5-1"]))
CLI_CASES.append(("playback_headphones_to_7_1", lambda: ["--playback-headphones-to-7-1"]))
CLI_CASES.append(("playback_enable_direct_mode", lambda: ["--playback-direct-mode", "Enabled"]))
CLI_CASES.append(("playback_enable_direct_mode", lambda: ["--playback-direct-mode", "Disabled"]))
CLI_CASES.append(("playback_enable_spdif_out_direct_mode", lambda: ["--playback-spdif-out-direct-mode", "Enabled"]))
CLI_CASES.append(("playback_enable_spdif_out_direct_mode", lambda: ["--playback-spdif-out-direct-mode", "Disabled"]))
for playback_filter in PlaybackFilter:
    CLI_CASES.append(("playback_filter", lambda pf=playback_filter: ["--playback-filter", pf.name]))

# ─── Decoder ───
CLI_CASES.append(("decoder_mode", lambda: ["--decoder-mode", "Normal"]))
CLI_CASES.append(("decoder_mode", lambda: ["--decoder-mode", "Full"]))
CLI_CASES.append(("decoder_mode", lambda: ["--decoder-mode", "Night"]))

# ─── Lighting ───
CLI_CASES.append(("lighting_disable", lambda: ["--lighting-disable"]))
CLI_CASES.append(("lighting_enable_set_rgb", lambda: ["--lighting-rgb", "0", "0", "0"]))
CLI_CASES.append(("lighting_enable_set_rgb", lambda: ["--lighting-rgb", "12", "34", "56"]))
CLI_CASES.append(("lighting_enable_set_rgb", lambda: ["--lighting-rgb", "255", "255", "255"]))

# ─── Mixer ───
CLI_CASES.append(("mixer_playback_mute", lambda: ["--mixer-playback-mute", "Enabled"]))
CLI_CASES.append(("mixer_playback_mute", lambda: ["--mixer-playback-mute", "Disabled"]))
CLI_CASES.append(("mixer_monitoring_line_in_mute", lambda: ["--mixer-monitoring-line-in-mute", "Enabled"]))
CLI_CASES.append(("mixer_monitoring_line_in_mute", lambda: ["--mixer-monitoring-line-in-mute", "Disabled"]))
CLI_CASES.append(("mixer_monitoring_line_in_volume", lambda: ["--mixer-monitoring-line-in-volume", "0"]))
CLI_CASES.append(("mixer_monitoring_line_in_volume", lambda: ["--mixer-monitoring-line-in-volume", "30"]))
CLI_CASES.append(("mixer_monitoring_line_in_volume", lambda: ["--mixer-monitoring-line-in-volume", "100"]))
CLI_CASES.append(("mixer_monitoring_external_mic_mute", lambda: ["--mixer-monitoring-external-mic-mute", "Enabled"]))
CLI_CASES.append(("mixer_monitoring_external_mic_mute", lambda: ["--mixer-monitoring-external-mic-mute", "Disabled"]))
CLI_CASES.append(("mixer_monitoring_external_mic_volume", lambda: ["--mixer-monitoring-external-mic-volume", "0"]))
CLI_CASES.append(("mixer_monitoring_external_mic_volume", lambda: ["--mixer-monitoring-external-mic-volume", "10"]))
CLI_CASES.append(("mixer_monitoring_external_mic_volume", lambda: ["--mixer-monitoring-external-mic-volume", "100"]))
CLI_CASES.append(("mixer_monitoring_spdif_in_mute", lambda: ["--mixer-monitoring-spdif-in-mute", "Enabled"]))
CLI_CASES.append(("mixer_monitoring_spdif_in_mute", lambda: ["--mixer-monitoring-spdif-in-mute", "Disabled"]))
CLI_CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ["--mixer-monitoring-spdif-in-volume", "0"]))
CLI_CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ["--mixer-monitoring-spdif-in-volume", "80"]))
CLI_CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ["--mixer-monitoring-spdif-in-volume", "100"]))
CLI_CASES.append(("mixer_recording_line_in_mute", lambda: ["--mixer-recording-line-in-mute", "Enabled"]))
CLI_CASES.append(("mixer_recording_line_in_mute", lambda: ["--mixer-recording-line-in-mute", "Disabled"]))
CLI_CASES.append(("mixer_recording_line_in_volume", lambda: ["--mixer-recording-line-in-volume", "0"]))
CLI_CASES.append(("mixer_recording_line_in_volume", lambda: ["--mixer-recording-line-in-volume", "60"]))
CLI_CASES.append(("mixer_recording_line_in_volume", lambda: ["--mixer-recording-line-in-volume", "100"]))
CLI_CASES.append(("mixer_recording_external_mic_mute", lambda: ["--mixer-recording-external-mic-mute", "Enabled"]))
CLI_CASES.append(("mixer_recording_external_mic_mute", lambda: ["--mixer-recording-external-mic-mute", "Disabled"]))
CLI_CASES.append(("mixer_recording_external_mic_volume", lambda: ["--mixer-recording-external-mic-volume", "0"]))
CLI_CASES.append(("mixer_recording_external_mic_volume", lambda: ["--mixer-recording-external-mic-volume", "70"]))
CLI_CASES.append(("mixer_recording_external_mic_volume", lambda: ["--mixer-recording-external-mic-volume", "100"]))
CLI_CASES.append(("mixer_recording_spdif_in_mute", lambda: ["--mixer-recording-spdif-in-mute", "Enabled"]))
CLI_CASES.append(("mixer_recording_spdif_in_mute", lambda: ["--mixer-recording-spdif-in-mute", "Disabled"]))
CLI_CASES.append(("mixer_recording_spdif_in_volume", lambda: ["--mixer-recording-spdif-in-volume", "0"]))
CLI_CASES.append(("mixer_recording_spdif_in_volume", lambda: ["--mixer-recording-spdif-in-volume", "10"]))
CLI_CASES.append(("mixer_recording_spdif_in_volume", lambda: ["--mixer-recording-spdif-in-volume", "100"]))
CLI_CASES.append(("mixer_recording_what_u_hear_mute", lambda: ["--mixer-recording-what-u-hear-mute", "Enabled"]))
CLI_CASES.append(("mixer_recording_what_u_hear_mute", lambda: ["--mixer-recording-what-u-hear-mute", "Disabled"]))
CLI_CASES.append(("mixer_recording_what_u_hear_volume", lambda: ["--mixer-recording-what-u-hear-volume", "0"]))
CLI_CASES.append(("mixer_recording_what_u_hear_volume", lambda: ["--mixer-recording-what-u-hear-volume", "40"]))
CLI_CASES.append(("mixer_recording_what_u_hear_volume", lambda: ["--mixer-recording-what-u-hear-volume", "100"]))

# ─── Recording ───
CLI_CASES.append(("recording_mute", lambda: ["--recording-mute", "Enabled"]))
CLI_CASES.append(("recording_mute", lambda: ["--recording-mute", "Disabled"]))
CLI_CASES.append(("recording_mic_recording_volume", lambda: ["--recording-mic-recording-volume", "0"]))
CLI_CASES.append(("recording_mic_recording_volume", lambda: ["--recording-mic-recording-volume", "30"]))
CLI_CASES.append(("recording_mic_recording_volume", lambda: ["--recording-mic-recording-volume", "100"]))
CLI_CASES.append(("recording_mic_boost", lambda: ["--recording-mic-boost-db", "0"]))
CLI_CASES.append(("recording_mic_boost", lambda: ["--recording-mic-boost-db", "10"]))
CLI_CASES.append(("recording_mic_boost", lambda: ["--recording-mic-boost-db", "20"]))
CLI_CASES.append(("recording_mic_boost", lambda: ["--recording-mic-boost-db", "30"]))
CLI_CASES.append(("recording_mic_monitoring_mute", lambda: ["--recording-mic-monitoring-mute", "Enabled"]))
CLI_CASES.append(("recording_mic_monitoring_mute", lambda: ["--recording-mic-monitoring-mute", "Disabled"]))
CLI_CASES.append(("recording_mic_monitoring_volume", lambda: ["--recording-mic-monitoring-volume", "0"]))
CLI_CASES.append(("recording_mic_monitoring_volume", lambda: ["--recording-mic-monitoring-volume", "70"]))
CLI_CASES.append(("recording_mic_monitoring_volume", lambda: ["--recording-mic-monitoring-volume", "100"]))
CLI_CASES.append(("recording_voice_clarity_noise_reduction_enabled", lambda: ["--recording-voice-clarity-noise-reduction", "Enabled"]))
CLI_CASES.append(("recording_voice_clarity_noise_reduction_enabled", lambda: ["--recording-voice-clarity-noise-reduction", "Disabled"]))
CLI_CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ["--recording-voice-clarity-noise-reduction-level", "0"]))
CLI_CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ["--recording-voice-clarity-noise-reduction-level", "40"]))
CLI_CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ["--recording-voice-clarity-noise-reduction-level", "100"]))
CLI_CASES.append(("recording_voice_clarity_acoustic_echo_cancellation_enabled", lambda: ["--recording-voice-clarity-aec", "Enabled"]))
CLI_CASES.append(("recording_voice_clarity_acoustic_echo_cancellation_enabled", lambda: ["--recording-voice-clarity-aec", "Disabled"]))
CLI_CASES.append(("recording_voice_clarity_smart_volume_enabled", lambda: ["--recording-voice-clarity-smart-volume", "Enabled"]))
CLI_CASES.append(("recording_voice_clarity_smart_volume_enabled", lambda: ["--recording-voice-clarity-smart-volume", "Disabled"]))
CLI_CASES.append(("recording_voice_clarity_mic_equalizer_enabled", lambda: ["--recording-voice-clarity-mic-eq", "Enabled"]))
CLI_CASES.append(("recording_voice_clarity_mic_equalizer_enabled", lambda: ["--recording-voice-clarity-mic-eq", "Disabled"]))
for preset in MicrophoneEqualizerPreset:
    CLI_CASES.append(("recording_voice_clarity_mic_equalizer_preset", lambda p=preset: ["--recording-voice-clarity-mic-eq-preset", p.name]))

# ─── SBX ───
CLI_CASES.append(("sbx_profile_switch", lambda: ["--sbx-profile-switch", "Special"]))
CLI_CASES.append(("sbx_surround_enabled", lambda: ["--sbx-profile", "Special", "--sbx-surround", "Enabled"]))
CLI_CASES.append(("sbx_surround_enabled", lambda: ["--sbx-profile", "Special", "--sbx-surround", "Enabled"]))
CLI_CASES.append(("sbx_surround_disabled", lambda: ["--sbx-profile", "Special", "--sbx-surround", "Disabled"]))
CLI_CASES.append(("sbx_surround_value_0", lambda: ["--sbx-profile", "Special", "--sbx-surround-value", "0"]))
CLI_CASES.append(("sbx_surround_value_42", lambda: ["--sbx-profile", "Special", "--sbx-surround-value", "42"]))
CLI_CASES.append(("sbx_surround_value_100", lambda: ["--sbx-profile", "Special", "--sbx-surround-value", "100"]))
CLI_CASES.append(("sbx_crystalizer_enabled", lambda: ["--sbx-profile", "Special", "--sbx-crystalizer", "Enabled"]))
CLI_CASES.append(("sbx_crystalizer_disabled", lambda: ["--sbx-profile", "Special", "--sbx-crystalizer", "Disabled"]))
CLI_CASES.append(("sbx_crystalizer_value_0", lambda: ["--sbx-profile", "Special", "--sbx-crystalizer-value", "0"]))
CLI_CASES.append(("sbx_crystalizer_value_42", lambda: ["--sbx-profile", "Special", "--sbx-crystalizer-value", "42"]))
CLI_CASES.append(("sbx_crystalizer_value_100", lambda: ["--sbx-profile", "Special", "--sbx-crystalizer-value", "100"]))
CLI_CASES.append(("sbx_bass_enabled", lambda: ["--sbx-profile", "Special", "--sbx-bass", "Enabled"]))
CLI_CASES.append(("sbx_bass_disabled", lambda: ["--sbx-profile", "Special", "--sbx-bass", "Disabled"]))
CLI_CASES.append(("sbx_bass_value_0", lambda: ["--sbx-profile", "Special", "--sbx-bass-value", "0"]))
CLI_CASES.append(("sbx_bass_value_42", lambda: ["--sbx-profile", "Special", "--sbx-bass-value", "42"]))
CLI_CASES.append(("sbx_bass_value_100", lambda: ["--sbx-profile", "Special", "--sbx-bass-value", "100"]))
CLI_CASES.append(("sbx_smart_volume_enabled", lambda: ["--sbx-profile", "Special", "--sbx-smart-volume", "Enabled"]))
CLI_CASES.append(("sbx_smart_volume_disabled", lambda: ["--sbx-profile", "Special", "--sbx-smart-volume", "Disabled"]))
CLI_CASES.append(("sbx_smart_volume_value_0", lambda: ["--sbx-profile", "Special", "--sbx-smart-volume-value", "0"]))
CLI_CASES.append(("sbx_smart_volume_value_42", lambda: ["--sbx-profile", "Special", "--sbx-smart-volume-value", "42"]))
CLI_CASES.append(("sbx_smart_volume_value_100", lambda: ["--sbx-profile", "Special", "--sbx-smart-volume-value", "100"]))
CLI_CASES.append(("sbx_smart_volume_special", lambda: ["--sbx-profile", "Special", "--sbx-smart-volume-special-value", "Night"]))
CLI_CASES.append(("sbx_smart_volume_special", lambda: ["--sbx-profile", "Special", "--sbx-smart-volume-special-value", "Loud"]))
CLI_CASES.append(("sbx_dialog_plus_enabled", lambda: ["--sbx-profile", "Special", "--sbx-dialog-plus", "Enabled"]))
CLI_CASES.append(("sbx_dialog_plus_disabled", lambda: ["--sbx-profile", "Special", "--sbx-dialog-plus", "Disabled"]))
CLI_CASES.append(("sbx_dialog_plus_value_0", lambda: ["--sbx-profile", "Special", "--sbx-dialog-plus-value", "0"]))
CLI_CASES.append(("sbx_dialog_plus_value_42", lambda: ["--sbx-profile", "Special", "--sbx-dialog-plus-value", "42"]))
CLI_CASES.append(("sbx_dialog_plus_value_100", lambda: ["--sbx-profile", "Special", "--sbx-dialog-plus-value", "100"]))
# @formatter:on


@pytest.mark.parametrize(
    "case_name,args_list_factory",
    CLI_CASES,
    ids=[f"{i}__{case_name}" for i, (case_name, _) in enumerate(CLI_CASES)])
def test_cli_cases(
        monkeypatch: pytest.MonkeyPatch,
        case_name: str,
        args_list_factory: ArgsListFactory,
) -> None:
    """
    Integration-style unit test:
    - uses the real CLI argument parsing
    - uses the real G6Api with dry_run=True
    - relies on --dry-run CLI flag to avoid hardware I/O
    """
    args_list = args_list_factory()

    # Mock sys.argv to simulate CLI invocation with --dry-run
    monkeypatch.setattr("sys.argv", ["g6-cli", "--dry-run", "--debug", "--no-persist"] + args_list)

    # Execute CLI main (should not raise any errors)
    result = cli_main()

    assert result is None
