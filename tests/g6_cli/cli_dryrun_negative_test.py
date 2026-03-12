from __future__ import annotations

from collections.abc import Callable

import sys

import pytest

from g6_cli import main as cli_main

# args_list returns list of CLI argument strings
ArgsListFactory = Callable[[], list[str]]

# noinspection PyListCreation
NEGATIVE_CLI_CASES: list[tuple[str, ArgsListFactory, str]] = []

# @formatter:off
# ─── Playback ───
NEGATIVE_CLI_CASES.append(("set_output_invalid", lambda: ["--set-output", "Bar"], "invalid choice: 'Bar' (choose from 'Speakers', 'Headphones')"))
NEGATIVE_CLI_CASES.append(("playback_mute_invalid", lambda: ["--playback-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
NEGATIVE_CLI_CASES.append(("playback_volume_invalid_low", lambda: ["--playback-volume", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("playback_volume_invalid_high", lambda: ["--playback-volume", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("playback_volume_invalid_type", lambda: ["--playback-volume", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("playback_volume_channels_invalid", lambda: ["--playback-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
NEGATIVE_CLI_CASES.append(("playback_direct_mode_invalid", lambda: ["--playback-direct-mode", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
NEGATIVE_CLI_CASES.append(("playback_spdif_out_direct_mode_invalid", lambda: ["--playback-spdif-out-direct-mode", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
NEGATIVE_CLI_CASES.append(("playback_filter_invalid", lambda: ["--playback-filter", "BAR"], "invalid choice: 'BAR'"))

# ─── Decoder ───
NEGATIVE_CLI_CASES.append(("decoder_mode_invalid", lambda: ["--decoder-mode", "Bar"], "invalid choice: 'Bar' (choose from 'Normal', 'Full', 'Night')"))

# ─── Lighting ───
NEGATIVE_CLI_CASES.append(("lighting_rgb_missing_arg", lambda: ["--lighting-rgb", "0", "0"], "expected 3 arguments"))
NEGATIVE_CLI_CASES.append(("lighting_rgb_extra_arg", lambda: ["--lighting-rgb", "0", "0", "0", "0"], "unrecognized arguments: 0"))
NEGATIVE_CLI_CASES.append(("lighting_rgb_invalid_type", lambda: ["--lighting-rgb", "0", "bar", "0"], "invalid int value: 'bar'"))

# ─── Mixer ───
NEGATIVE_CLI_CASES.append(("mixer_playback_mute_invalid", lambda: ["--mixer-playback-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
NEGATIVE_CLI_CASES.append(("mixer_monitoring_line_in_volume_invalid", lambda: ["--mixer-monitoring-line-in-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
NEGATIVE_CLI_CASES.append(("mixer_monitoring_line_in_volume_low", lambda: ["--mixer-monitoring-line-in-volume", "-10"], "invalid choice: -10 (choose from 0, 10, 20,"))
NEGATIVE_CLI_CASES.append(("mixer_monitoring_line_in_volume_high", lambda: ["--mixer-monitoring-line-in-volume", "110"], "invalid choice: 110 (choose from 0, 10, 20,"))
NEGATIVE_CLI_CASES.append(("mixer_monitoring_line_in_volume_type", lambda: ["--mixer-monitoring-line-in-volume", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("mixer_monitoring_line_in_volume_channels_invalid", lambda: ["--mixer-monitoring-line-in-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
NEGATIVE_CLI_CASES.append(("mixer_monitoring_external_mic_volume_invalid", lambda: ["--mixer-monitoring-external-mic-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
NEGATIVE_CLI_CASES.append(("mixer_monitoring_external_mic_volume_type", lambda: ["--mixer-monitoring-external-mic-volume", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("mixer_monitoring_external_mic_volume_channels_invalid", lambda: ["--mixer-monitoring-external-mic-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
NEGATIVE_CLI_CASES.append(("mixer_recording_line_in_volume_invalid", lambda: ["--mixer-recording-line-in-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
NEGATIVE_CLI_CASES.append(("mixer_recording_line_in_volume_type", lambda: ["--mixer-recording-line-in-volume", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("mixer_recording_line_in_volume_channels_invalid", lambda: ["--mixer-recording-line-in-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
NEGATIVE_CLI_CASES.append(("mixer_recording_external_mic_volume_invalid", lambda: ["--mixer-recording-external-mic-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
NEGATIVE_CLI_CASES.append(("mixer_recording_external_mic_volume_type", lambda: ["--mixer-recording-external-mic-volume", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("mixer_recording_external_mic_volume_channels_invalid", lambda: ["--mixer-recording-external-mic-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
NEGATIVE_CLI_CASES.append(("mixer_recording_spdif_in_volume_invalid", lambda: ["--mixer-recording-spdif-in-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
NEGATIVE_CLI_CASES.append(("mixer_recording_spdif_in_volume_type", lambda: ["--mixer-recording-spdif-in-volume", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("mixer_recording_spdif_in_volume_channels_invalid", lambda: ["--mixer-recording-spdif-in-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
NEGATIVE_CLI_CASES.append(("mixer_recording_what_u_hear_volume_invalid", lambda: ["--mixer-recording-what-u-hear-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
NEGATIVE_CLI_CASES.append(("mixer_recording_what_u_hear_volume_type", lambda: ["--mixer-recording-what-u-hear-volume", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("mixer_recording_what_u_hear_volume_channels_invalid", lambda: ["--mixer-recording-what-u-hear-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))

# ─── Recording ───
NEGATIVE_CLI_CASES.append(("recording_mic_recording_volume_invalid", lambda: ["--recording-mic-recording-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
NEGATIVE_CLI_CASES.append(("recording_mic_recording_volume_type", lambda: ["--recording-mic-recording-volume", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("recording_mic_boost_invalid", lambda: ["--recording-mic-boost-db", "5"], "invalid choice: 5 (choose from 0, 10, 20, 30)"))
NEGATIVE_CLI_CASES.append(("recording_mic_boost_low", lambda: ["--recording-mic-boost-db", "-10"], "invalid choice: -10 (choose from 0, 10, 20, 30)"))
NEGATIVE_CLI_CASES.append(("recording_mic_boost_high", lambda: ["--recording-mic-boost-db", "40"], "invalid choice: 40 (choose from 0, 10, 20, 30)"))
NEGATIVE_CLI_CASES.append(("recording_mic_boost_type", lambda: ["--recording-mic-boost-db", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("recording_mic_monitoring_volume_invalid", lambda: ["--recording-mic-monitoring-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
NEGATIVE_CLI_CASES.append(("recording_mic_monitoring_volume_type", lambda: ["--recording-mic-monitoring-volume", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("recording_voice_clarity_noise_reduction_invalid", lambda: ["--recording-voice-clarity-noise-reduction", "10"], "invalid choice: 10 (choose from 0, 20, 40, 60, 80, 100)"))
NEGATIVE_CLI_CASES.append(("recording_voice_clarity_noise_reduction_low", lambda: ["--recording-voice-clarity-noise-reduction", "-20"], "invalid choice: -20 (choose from 0, 20, 40, 60, 80, 100)"))
NEGATIVE_CLI_CASES.append(("recording_voice_clarity_noise_reduction_high", lambda: ["--recording-voice-clarity-noise-reduction", "120"], "invalid choice: 120 (choose from 0, 20, 40, 60, 80, 100)"))
NEGATIVE_CLI_CASES.append(("recording_voice_clarity_noise_reduction_type", lambda: ["--recording-voice-clarity-noise-reduction", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("recording_voice_clarity_mic_eq_preset_invalid", lambda: ["--recording-voice-clarity-mic-eq-preset", "BAR"], "invalid choice: 'BAR'"))

# ─── SBX ───
NEGATIVE_CLI_CASES.append(("sbx_surround_value_low", lambda: ["--sbx-surround-value", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("sbx_surround_value_high", lambda: ["--sbx-surround-value", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("sbx_surround_value_type", lambda: ["--sbx-surround-value", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("sbx_crystalizer_value_low", lambda: ["--sbx-crystalizer-value", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("sbx_crystalizer_value_high", lambda: ["--sbx-crystalizer-value", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("sbx_crystalizer_value_type", lambda: ["--sbx-crystalizer-value", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("sbx_bass_value_low", lambda: ["--sbx-bass-value", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("sbx_bass_value_high", lambda: ["--sbx-bass-value", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("sbx_bass_value_type", lambda: ["--sbx-bass-value", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("sbx_smart_volume_value_low", lambda: ["--sbx-smart-volume-value", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("sbx_smart_volume_value_high", lambda: ["--sbx-smart-volume-value", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("sbx_smart_volume_value_type", lambda: ["--sbx-smart-volume-value", "bar"], "invalid int value: 'bar'"))
NEGATIVE_CLI_CASES.append(("sbx_smart_volume_special_value_invalid", lambda: ["--sbx-smart-volume-special-value", "Bar"], "invalid choice: 'Bar' (choose from 'Night', 'Loud')"))
NEGATIVE_CLI_CASES.append(("sbx_dialog_plus_value_low", lambda: ["--sbx-dialog-plus-value", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("sbx_dialog_plus_value_high", lambda: ["--sbx-dialog-plus-value", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
NEGATIVE_CLI_CASES.append(("sbx_dialog_plus_value_type", lambda: ["--sbx-dialog-plus-value", "bar"], "invalid int value: 'bar'"))
# @formatter:on


@pytest.mark.parametrize(
    "case_name,args_list_factory,expected_error_snippet",
    NEGATIVE_CLI_CASES,
    ids=[f"{i}__{case_name}__{'-'.join(args_list_factory())}" for i, (case_name, args_list_factory, _) in
         enumerate(NEGATIVE_CLI_CASES)],
)
def test_cli_invalid_arguments_raise_argparse_error_in_dry_run(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
        case_name: str,
        args_list_factory: ArgsListFactory,
        expected_error_snippet: str,
) -> None:
    """
    Verify that invalid CLI arguments cause argparse to exit with SystemExit
    and print a meaningful error message — even when --dry-run is active.
    """
    args_list = args_list_factory()

    # Simulate CLI invocation with --dry-run + invalid arguments
    monkeypatch.setattr(sys, "argv", ["g6-cli", "--dry-run", "--no-persist"] + args_list)

    # argparse validation should raise SystemExit (usually code 2)
    with pytest.raises(SystemExit) as exit_info:
        cli_main()
    assert exit_info.value.code == 2

    captured = capsys.readouterr()
    assert expected_error_snippet in captured.err, (
        f"Expected error snippet '{expected_error_snippet}' not found in stderr.\n"
        f"Actual stderr:\n{captured.err}"
    )
