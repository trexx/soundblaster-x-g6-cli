from __future__ import annotations

from collections.abc import Callable

import pytest

from g6_cli import main as cli_main
from g6_cli.g6_spec import PlaybackFilter
from g6_cli.g6_spec.recording import MicrophoneEqualizerPreset

# args_list returns list of CLI argument strings
ArgsListFactory = Callable[[], list[str]]

# noinspection PyListCreation
CASES: list[tuple[str, ArgsListFactory]] = []

# @formatter:off
# ─── Device / services ───
CASES.append(("reload_alsa_and_pipewire", lambda: ["--reload-audio-services"]))
CASES.append(("reload_alsa_and_pipewire", lambda: ["--reload-audio-services", "--reload-audio-services-no-sudo"]))

# ─── Playback ───
CASES.append(("playback_toggle_to_speakers", lambda: ["--set-output", "Speakers"]))
CASES.append(("playback_toggle_to_headphones", lambda: ["--set-output", "Headphones"]))
CASES.append(("playback_toggle_to_speakers", lambda: ["--toggle-output"]))
CASES.append(("playback_mute", lambda: ["--playback-mute", "Enabled"]))
CASES.append(("playback_mute", lambda: ["--playback-mute", "Disabled"]))
CASES.append(("playback_volume", lambda: ["--playback-volume", "0"]))
CASES.append(("playback_volume", lambda: ["--playback-volume", "50"]))
CASES.append(("playback_volume", lambda: ["--playback-volume", "100"]))
CASES.append(("playback_volume", lambda: ["--playback-volume", "50", "--playback-volume-channels", "Left"]))
CASES.append(("playback_volume", lambda: ["--playback-volume", "50", "--playback-volume-channels", "Right"]))
CASES.append(("playback_speakers_to_stereo", lambda: ["--playback-speakers-to-stereo"]))
CASES.append(("playback_speakers_to_5_1", lambda: ["--playback-speakers-to-5-1"]))
CASES.append(("playback_speakers_to_7_1", lambda: ["--playback-speakers-to-7-1"]))
CASES.append(("playback_headphones_to_stereo", lambda: ["--playback-headphones-to-stereo"]))
CASES.append(("playback_headphones_to_5_1", lambda: ["--playback-headphones-to-5-1"]))
CASES.append(("playback_headphones_to_7_1", lambda: ["--playback-headphones-to-7-1"]))
CASES.append(("playback_enable_direct_mode", lambda: ["--playback-direct-mode", "Enabled"]))
CASES.append(("playback_enable_direct_mode", lambda: ["--playback-direct-mode", "Disabled"]))
CASES.append(("playback_enable_spdif_out_direct_mode", lambda: ["--playback-spdif-out-direct-mode", "Enabled"]))
CASES.append(("playback_enable_spdif_out_direct_mode", lambda: ["--playback-spdif-out-direct-mode", "Disabled"]))
for playback_filter in PlaybackFilter:
    CASES.append(("playback_filter", lambda pf=playback_filter: ["--playback-filter", pf.name]))

# ─── Decoder ───
CASES.append(("decoder_mode", lambda: ["--decoder-mode", "Normal"]))
CASES.append(("decoder_mode", lambda: ["--decoder-mode", "Full"]))
CASES.append(("decoder_mode", lambda: ["--decoder-mode", "Night"]))

# ─── Lighting ───
CASES.append(("lighting_disable", lambda: ["--lighting-disable"]))
CASES.append(("lighting_enable_set_rgb", lambda: ["--lighting-rgb", "0", "0", "0"]))
CASES.append(("lighting_enable_set_rgb", lambda: ["--lighting-rgb", "12", "34", "56"]))
CASES.append(("lighting_enable_set_rgb", lambda: ["--lighting-rgb", "255", "255", "255"]))

# ─── Mixer ───
CASES.append(("mixer_playback_mute", lambda: ["--mixer-playback-mute", "Enabled"]))
CASES.append(("mixer_playback_mute", lambda: ["--mixer-playback-mute", "Disabled"]))
CASES.append(("mixer_monitoring_line_in_mute", lambda: ["--mixer-monitoring-line-in-mute", "Enabled"]))
CASES.append(("mixer_monitoring_line_in_mute", lambda: ["--mixer-monitoring-line-in-mute", "Disabled"]))
CASES.append(("mixer_monitoring_line_in_volume", lambda: ["--mixer-monitoring-line-in-volume", "0"]))
CASES.append(("mixer_monitoring_line_in_volume", lambda: ["--mixer-monitoring-line-in-volume", "30"]))
CASES.append(("mixer_monitoring_line_in_volume", lambda: ["--mixer-monitoring-line-in-volume", "100"]))
CASES.append(("mixer_monitoring_external_mic_mute", lambda: ["--mixer-monitoring-external-mic-mute", "Enabled"]))
CASES.append(("mixer_monitoring_external_mic_mute", lambda: ["--mixer-monitoring-external-mic-mute", "Disabled"]))
CASES.append(("mixer_monitoring_external_mic_volume", lambda: ["--mixer-monitoring-external-mic-volume", "0"]))
CASES.append(("mixer_monitoring_external_mic_volume", lambda: ["--mixer-monitoring-external-mic-volume", "10"]))
CASES.append(("mixer_monitoring_external_mic_volume", lambda: ["--mixer-monitoring-external-mic-volume", "100"]))
CASES.append(("mixer_monitoring_spdif_in_mute", lambda: ["--mixer-monitoring-spdif-in-mute", "Enabled"]))
CASES.append(("mixer_monitoring_spdif_in_mute", lambda: ["--mixer-monitoring-spdif-in-mute", "Disabled"]))
CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ["--mixer-monitoring-spdif-in-volume", "0"]))
CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ["--mixer-monitoring-spdif-in-volume", "80"]))
CASES.append(("mixer_monitoring_spdif_in_volume", lambda: ["--mixer-monitoring-spdif-in-volume", "100"]))
CASES.append(("mixer_recording_line_in_mute", lambda: ["--mixer-recording-line-in-mute", "Enabled"]))
CASES.append(("mixer_recording_line_in_mute", lambda: ["--mixer-recording-line-in-mute", "Disabled"]))
CASES.append(("mixer_recording_line_in_volume", lambda: ["--mixer-recording-line-in-volume", "0"]))
CASES.append(("mixer_recording_line_in_volume", lambda: ["--mixer-recording-line-in-volume", "60"]))
CASES.append(("mixer_recording_line_in_volume", lambda: ["--mixer-recording-line-in-volume", "100"]))
CASES.append(("mixer_recording_external_mic_mute", lambda: ["--mixer-recording-external-mic-mute", "Enabled"]))
CASES.append(("mixer_recording_external_mic_mute", lambda: ["--mixer-recording-external-mic-mute", "Disabled"]))
CASES.append(("mixer_recording_external_mic_volume", lambda: ["--mixer-recording-external-mic-volume", "0"]))
CASES.append(("mixer_recording_external_mic_volume", lambda: ["--mixer-recording-external-mic-volume", "70"]))
CASES.append(("mixer_recording_external_mic_volume", lambda: ["--mixer-recording-external-mic-volume", "100"]))
CASES.append(("mixer_recording_spdif_in_mute", lambda: ["--mixer-recording-spdif-in-mute", "Enabled"]))
CASES.append(("mixer_recording_spdif_in_mute", lambda: ["--mixer-recording-spdif-in-mute", "Disabled"]))
CASES.append(("mixer_recording_spdif_in_volume", lambda: ["--mixer-recording-spdif-in-volume", "0"]))
CASES.append(("mixer_recording_spdif_in_volume", lambda: ["--mixer-recording-spdif-in-volume", "10"]))
CASES.append(("mixer_recording_spdif_in_volume", lambda: ["--mixer-recording-spdif-in-volume", "100"]))
CASES.append(("mixer_recording_what_u_hear_mute", lambda: ["--mixer-recording-what-u-hear-mute", "Enabled"]))
CASES.append(("mixer_recording_what_u_hear_mute", lambda: ["--mixer-recording-what-u-hear-mute", "Disabled"]))
CASES.append(("mixer_recording_what_u_hear_volume", lambda: ["--mixer-recording-what-u-hear-volume", "0"]))
CASES.append(("mixer_recording_what_u_hear_volume", lambda: ["--mixer-recording-what-u-hear-volume", "40"]))
CASES.append(("mixer_recording_what_u_hear_volume", lambda: ["--mixer-recording-what-u-hear-volume", "100"]))

# ─── Recording ───
CASES.append(("recording_mute", lambda: ["--recording-mute", "Enabled"]))
CASES.append(("recording_mute", lambda: ["--recording-mute", "Disabled"]))
CASES.append(("recording_mic_recording_volume", lambda: ["--recording-mic-recording-volume", "0"]))
CASES.append(("recording_mic_recording_volume", lambda: ["--recording-mic-recording-volume", "30"]))
CASES.append(("recording_mic_recording_volume", lambda: ["--recording-mic-recording-volume", "100"]))
CASES.append(("recording_mic_boost", lambda: ["--recording-mic-boost-db", "0"]))
CASES.append(("recording_mic_boost", lambda: ["--recording-mic-boost-db", "10"]))
CASES.append(("recording_mic_boost", lambda: ["--recording-mic-boost-db", "20"]))
CASES.append(("recording_mic_boost", lambda: ["--recording-mic-boost-db", "30"]))
CASES.append(("recording_mic_monitoring_mute", lambda: ["--recording-mic-monitoring-mute", "Enabled"]))
CASES.append(("recording_mic_monitoring_mute", lambda: ["--recording-mic-monitoring-mute", "Disabled"]))
CASES.append(("recording_mic_monitoring_volume", lambda: ["--recording-mic-monitoring-volume", "0"]))
CASES.append(("recording_mic_monitoring_volume", lambda: ["--recording-mic-monitoring-volume", "70"]))
CASES.append(("recording_mic_monitoring_volume", lambda: ["--recording-mic-monitoring-volume", "100"]))
CASES.append(("recording_voice_clarity_enabled", lambda: ["--recording-voice-clarity", "Enabled"]))
CASES.append(("recording_voice_clarity_enabled", lambda: ["--recording-voice-clarity", "Disabled"]))
CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ["--recording-voice-clarity-noise-reduction", "0"]))
CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ["--recording-voice-clarity-noise-reduction", "40"]))
CASES.append(("recording_voice_clarity_noise_reduction_level", lambda: ["--recording-voice-clarity-noise-reduction", "100"]))
CASES.append(("recording_voice_clarity_acoustic_echo_cancellation_enabled", lambda: ["--recording-voice-clarity-aec", "Enabled"]))
CASES.append(("recording_voice_clarity_acoustic_echo_cancellation_enabled", lambda: ["--recording-voice-clarity-aec", "Disabled"]))
CASES.append(("recording_voice_clarity_smart_volume_enabled", lambda: ["--recording-voice-clarity-smart-volume", "Enabled"]))
CASES.append(("recording_voice_clarity_smart_volume_enabled", lambda: ["--recording-voice-clarity-smart-volume", "Disabled"]))
CASES.append(("recording_voice_clarity_mic_equalizer_enabled", lambda: ["--recording-voice-clarity-mic-eq", "Enabled"]))
CASES.append(("recording_voice_clarity_mic_equalizer_enabled", lambda: ["--recording-voice-clarity-mic-eq", "Disabled"]))
for preset in MicrophoneEqualizerPreset:
    CASES.append(("recording_voice_clarity_mic_equalizer_preset", lambda p=preset: ["--recording-voice-clarity-mic-eq-preset", p.name]))

# ─── SBX ───
CASES.append(("sbx_toggle", lambda: ["--sbx-surround", "Enabled"]))
CASES.append(("sbx_toggle", lambda: ["--sbx-surround", "Disabled"]))
CASES.append(("sbx_slider", lambda: ["--sbx-surround-value", "0"]))
CASES.append(("sbx_slider", lambda: ["--sbx-surround-value", "42"]))
CASES.append(("sbx_slider", lambda: ["--sbx-surround-value", "100"]))
CASES.append(("sbx_toggle", lambda: ["--sbx-crystalizer", "Enabled"]))
CASES.append(("sbx_toggle", lambda: ["--sbx-crystalizer", "Disabled"]))
CASES.append(("sbx_slider", lambda: ["--sbx-crystalizer-value", "0"]))
CASES.append(("sbx_slider", lambda: ["--sbx-crystalizer-value", "42"]))
CASES.append(("sbx_slider", lambda: ["--sbx-crystalizer-value", "100"]))
CASES.append(("sbx_toggle", lambda: ["--sbx-bass", "Enabled"]))
CASES.append(("sbx_toggle", lambda: ["--sbx-bass", "Disabled"]))
CASES.append(("sbx_slider", lambda: ["--sbx-bass-value", "0"]))
CASES.append(("sbx_slider", lambda: ["--sbx-bass-value", "42"]))
CASES.append(("sbx_slider", lambda: ["--sbx-bass-value", "100"]))
CASES.append(("sbx_toggle", lambda: ["--sbx-smart-volume", "Enabled"]))
CASES.append(("sbx_toggle", lambda: ["--sbx-smart-volume", "Disabled"]))
CASES.append(("sbx_slider", lambda: ["--sbx-smart-volume-value", "0"]))
CASES.append(("sbx_slider", lambda: ["--sbx-smart-volume-value", "42"]))
CASES.append(("sbx_slider", lambda: ["--sbx-smart-volume-value", "100"]))
CASES.append(("sbx_smart_volume_special", lambda: ["--sbx-smart-volume-special-value", "Night"]))
CASES.append(("sbx_smart_volume_special", lambda: ["--sbx-smart-volume-special-value", "Loud"]))
CASES.append(("sbx_toggle", lambda: ["--sbx-dialog-plus", "Enabled"]))
CASES.append(("sbx_toggle", lambda: ["--sbx-dialog-plus", "Disabled"]))
CASES.append(("sbx_slider", lambda: ["--sbx-dialog-plus-value", "0"]))
CASES.append(("sbx_slider", lambda: ["--sbx-dialog-plus-value", "42"]))
CASES.append(("sbx_slider", lambda: ["--sbx-dialog-plus-value", "100"]))
# @formatter:on


@pytest.mark.parametrize(
    "method_name,args_list_factory",
    CASES,
    ids=[f"{i}__{name}" for i, (name, _) in enumerate(CASES)])
def test_cli_commands_execute_in_dry_run_without_errors(
        monkeypatch: pytest.MonkeyPatch,
        method_name: str,
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
    monkeypatch.setattr("sys.argv", ["g6-cli", "--dry-run", "--debug"] + args_list)

    # Execute CLI main (should not raise any errors)
    result = cli_main()

    assert result is None
