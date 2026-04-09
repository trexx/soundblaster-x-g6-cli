from __future__ import annotations

from collections.abc import Callable

import sys
from unittest.mock import MagicMock

import pytest

from g6_cli import main as cli_main
import g6_cli.g6_api as g6_api
from g6_cli.g6_core import G6Device


@pytest.fixture()
def api(monkeypatch: pytest.MonkeyPatch) -> g6_api.G6Api:
    """
    Always construct with dry_run=True (per requirement) and never touch real hardware.
    """
    # mock detect_device() method on g6_api module level
    monkeypatch.setattr(g6_api, "detect_device", MagicMock(return_value=G6Device))
    return g6_api.G6Api(dry_run=True, debug=True, persist_model=False)


# args_list returns list of CLI argument strings
ArgsListFactory = Callable[[], list[str]]

# noinspection PyListCreation
ARGPARSE_ERROR_CLI_CASES: list[tuple[str, ArgsListFactory, str]] = []

# @formatter:off
# ─── Playback ───
ARGPARSE_ERROR_CLI_CASES.append(("set_output_invalid", lambda: ["--set-output", "Bar"], "invalid choice: 'Bar' (choose from 'Speakers', 'Headphones')"))
ARGPARSE_ERROR_CLI_CASES.append(("playback_mute_invalid", lambda: ["--playback-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("playback_volume_invalid_low", lambda: ["--playback-volume", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("playback_volume_invalid_high", lambda: ["--playback-volume", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("playback_volume_invalid_type", lambda: ["--playback-volume", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("playback_volume_channels_invalid", lambda: ["--playback-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
ARGPARSE_ERROR_CLI_CASES.append(("playback_direct_mode_invalid", lambda: ["--playback-direct-mode", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("playback_spdif_out_direct_mode_invalid", lambda: ["--playback-spdif-out-direct-mode", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("playback_filter_invalid", lambda: ["--playback-filter", "BAR"], "invalid choice: 'BAR'"))

# ─── Decoder ───
ARGPARSE_ERROR_CLI_CASES.append(("decoder_mode_invalid", lambda: ["--decoder-mode", "Bar"], "invalid choice: 'Bar' (choose from 'Normal', 'Full', 'Night')"))

# ─── Lighting ───
ARGPARSE_ERROR_CLI_CASES.append(("lighting_rgb_missing_arg", lambda: ["--lighting-rgb", "0", "0"], "expected 3 arguments"))
ARGPARSE_ERROR_CLI_CASES.append(("lighting_rgb_extra_arg", lambda: ["--lighting-rgb", "0", "0", "0", "0"], "unrecognized arguments: 0"))
ARGPARSE_ERROR_CLI_CASES.append(("lighting_rgb_invalid_type", lambda: ["--lighting-rgb", "0", "bar", "0"], "invalid int value: 'bar'"))

# ─── Mixer ───
ARGPARSE_ERROR_CLI_CASES.append(("mixer_playback_mute_invalid", lambda: ["--mixer-playback-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_line_in_mute_invalid", lambda: ["--mixer-monitoring-line-in-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_line_in_volume_invalid", lambda: ["--mixer-monitoring-line-in-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_line_in_volume_low", lambda: ["--mixer-monitoring-line-in-volume", "-10"], "invalid choice: -10 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_line_in_volume_high", lambda: ["--mixer-monitoring-line-in-volume", "110"], "invalid choice: 110 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_line_in_volume_type", lambda: ["--mixer-monitoring-line-in-volume", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_line_in_volume_channels_invalid", lambda: ["--mixer-monitoring-line-in-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_external_mic_mute_invalid", lambda: ["--mixer-monitoring-external-mic-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_external_mic_volume_invalid", lambda: ["--mixer-monitoring-external-mic-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_external_mic_volume_type", lambda: ["--mixer-monitoring-external-mic-volume", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_external_mic_volume_channels_invalid", lambda: ["--mixer-monitoring-external-mic-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_spdif_in_mute_invalid", lambda: ["--mixer-monitoring-spdif-in-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_spdif_in_volume_invalid", lambda: ["--mixer-monitoring-spdif-in-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_spdif_in_volume_type", lambda: ["--mixer-monitoring-spdif-in-volume", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_monitoring_spdif_in_volume_channels_invalid", lambda: ["--mixer-monitoring-spdif-in-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_line_in_mute_invalid", lambda: ["--mixer-recording-line-in-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_line_in_volume_invalid", lambda: ["--mixer-recording-line-in-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_line_in_volume_type", lambda: ["--mixer-recording-line-in-volume", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_line_in_volume_channels_invalid", lambda: ["--mixer-recording-line-in-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_external_mic_mute_invalid", lambda: ["--mixer-recording-external-mic-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_external_mic_volume_invalid", lambda: ["--mixer-recording-external-mic-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_external_mic_volume_type", lambda: ["--mixer-recording-external-mic-volume", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_external_mic_volume_channels_invalid", lambda: ["--mixer-recording-external-mic-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_spdif_in_mute_invalid", lambda: ["--mixer-recording-spdif-in-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_spdif_in_volume_invalid", lambda: ["--mixer-recording-spdif-in-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_spdif_in_volume_type", lambda: ["--mixer-recording-spdif-in-volume", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_spdif_in_volume_channels_invalid", lambda: ["--mixer-recording-spdif-in-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_what_u_hear_mute_invalid", lambda: ["--mixer-recording-what-u-hear-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_what_u_hear_volume_invalid", lambda: ["--mixer-recording-what-u-hear-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_what_u_hear_volume_type", lambda: ["--mixer-recording-what-u-hear-volume", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("mixer_recording_what_u_hear_volume_channels_invalid", lambda: ["--mixer-recording-what-u-hear-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))

# ─── Recording ───
ARGPARSE_ERROR_CLI_CASES.append(("recording_mute_invalid", lambda: ["--recording-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_recording_volume_invalid", lambda: ["--recording-mic-recording-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_recording_volume_type", lambda: ["--recording-mic-recording-volume", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_recording_volume_channels_invalid", lambda: ["--recording-mic-recording-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_boost_invalid", lambda: ["--recording-mic-boost-db", "5"], "invalid choice: 5 (choose from 0, 10, 20, 30)"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_boost_low", lambda: ["--recording-mic-boost-db", "-10"], "invalid choice: -10 (choose from 0, 10, 20, 30)"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_boost_high", lambda: ["--recording-mic-boost-db", "40"], "invalid choice: 40 (choose from 0, 10, 20, 30)"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_boost_type", lambda: ["--recording-mic-boost-db", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_monitoring_mute_invalid", lambda: ["--recording-mic-monitoring-mute", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_monitoring_volume_invalid", lambda: ["--recording-mic-monitoring-volume", "5"], "invalid choice: 5 (choose from 0, 10, 20,"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_monitoring_volume_type", lambda: ["--recording-mic-monitoring-volume", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_mic_monitoring_volume_channels_invalid", lambda: ["--recording-mic-monitoring-volume-channels", "Bar"], "invalid choice: 'Bar' (choose from 'Both', 'Left', 'Right')"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_voice_clarity_noise_reduction_invalid", lambda: ["--recording-voice-clarity-noise-reduction", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_voice_clarity_noise_reduction_level_invalid", lambda: ["--recording-voice-clarity-noise-reduction-level", "10"], "invalid choice: 10 (choose from 0, 20, 40, 60, 80, 100)"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_voice_clarity_noise_reduction_level_low", lambda: ["--recording-voice-clarity-noise-reduction-level", "-20"], "invalid choice: -20 (choose from 0, 20, 40, 60, 80, 100)"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_voice_clarity_noise_reduction_level_high", lambda: ["--recording-voice-clarity-noise-reduction-level", "120"], "invalid choice: 120 (choose from 0, 20, 40, 60, 80, 100)"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_voice_clarity_noise_reduction_level_type", lambda: ["--recording-voice-clarity-noise-reduction-level", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_voice_clarity_aec_invalid", lambda: ["--recording-voice-clarity-aec", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_voice_clarity_smart_volume_invalid", lambda: ["--recording-voice-clarity-smart-volume", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_voice_clarity_mic_eq_invalid", lambda: ["--recording-voice-clarity-mic-eq", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("recording_voice_clarity_mic_eq_preset_invalid", lambda: ["--recording-voice-clarity-mic-eq-preset", "BAR"], "invalid choice: 'BAR'"))

# ─── SBX ───
ARGPARSE_ERROR_CLI_CASES.append(("sbx_surround_invalid", lambda: ["--sbx-surround", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_surround_value_low", lambda: ["--sbx-surround-value", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_surround_value_high", lambda: ["--sbx-surround-value", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_surround_value_type", lambda: ["--sbx-surround-value", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_crystalizer_invalid", lambda: ["--sbx-crystalizer", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_crystalizer_value_low", lambda: ["--sbx-crystalizer-value", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_crystalizer_value_high", lambda: ["--sbx-crystalizer-value", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_crystalizer_value_type", lambda: ["--sbx-crystalizer-value", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_bass_invalid", lambda: ["--sbx-bass", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_bass_value_low", lambda: ["--sbx-bass-value", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_bass_value_high", lambda: ["--sbx-bass-value", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_bass_value_type", lambda: ["--sbx-bass-value", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_smart_volume_invalid", lambda: ["--sbx-smart-volume", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_smart_volume_value_low", lambda: ["--sbx-smart-volume-value", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_smart_volume_value_high", lambda: ["--sbx-smart-volume-value", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_smart_volume_value_type", lambda: ["--sbx-smart-volume-value", "bar"], "invalid int value: 'bar'"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_smart_volume_special_value_invalid", lambda: ["--sbx-smart-volume-special-value", "Bar"], "invalid choice: 'Bar' (choose from 'Night', 'Loud')"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_dialog_plus_invalid", lambda: ["--sbx-dialog-plus", "Bar"], "invalid choice: 'Bar' (choose from 'Enabled', 'Disabled')"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_dialog_plus_value_low", lambda: ["--sbx-dialog-plus-value", "-1"], "invalid choice: -1 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_dialog_plus_value_high", lambda: ["--sbx-dialog-plus-value", "101"], "invalid choice: 101 (choose from 0, 1, 2,"))
ARGPARSE_ERROR_CLI_CASES.append(("sbx_dialog_plus_value_type", lambda: ["--sbx-dialog-plus-value", "bar"], "invalid int value: 'bar'"))
# @formatter:on

# noinspection PyListCreation
MISSING_SBX_PROFILE_ERROR_MESSAGE = "The SBX profile to use must be specified with '--sbx-profile' when updating an SBX effect!"
VALUE_ERROR_CLI_CASES: list[tuple[str, ArgsListFactory, str]] = []
# @formatter:off
VALUE_ERROR_CLI_CASES.append(("sbx_profile_switch", lambda: ["--sbx-profile", "Special", "--sbx-profile-switch", "Special"], "Only one of --sbx-profile and --sbx_profile_switch may be specified!"))
VALUE_ERROR_CLI_CASES.append(("sbx_surround_enabled", lambda: ["--sbx-surround", "Enabled"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_surround_disabled", lambda: ["--sbx-surround", "Disabled"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_surround_value_0", lambda: ["--sbx-surround-value", "0"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_surround_value_42", lambda: ["--sbx-surround-value", "42"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_surround_value_100", lambda: ["--sbx-surround-value", "100"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_crystalizer_enabled", lambda: ["--sbx-crystalizer", "Enabled"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_crystalizer_disabled", lambda: ["--sbx-crystalizer", "Disabled"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_crystalizer_value_0", lambda: ["--sbx-crystalizer-value", "0"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_crystalizer_value_42", lambda: ["--sbx-crystalizer-value", "42"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_crystalizer_value_100", lambda: ["--sbx-crystalizer-value", "100"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_bass_enabled", lambda: ["--sbx-bass", "Enabled"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_bass_disabled", lambda: ["--sbx-bass", "Disabled"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_bass_value_0", lambda: ["--sbx-bass-value", "0"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_bass_value_42", lambda: ["--sbx-bass-value", "42"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_bass_value_100", lambda: ["--sbx-bass-value", "100"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_smart_volume_enabled", lambda: ["--sbx-smart-volume", "Enabled"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_smart_volume_disabled", lambda: ["--sbx-smart-volume", "Disabled"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_smart_volume_value_0", lambda: ["--sbx-smart-volume-value", "0"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_smart_volume_value_42", lambda: ["--sbx-smart-volume-value", "42"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_smart_volume_value_100", lambda: ["--sbx-smart-volume-value", "100"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_smart_volume_special", lambda: ["--sbx-smart-volume-special-value", "Night"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_smart_volume_special", lambda: ["--sbx-smart-volume-special-value", "Loud"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_dialog_plus_enabled", lambda: ["--sbx-dialog-plus", "Enabled"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_dialog_plus_disabled", lambda: ["--sbx-dialog-plus", "Disabled"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_dialog_plus_value_0", lambda: ["--sbx-dialog-plus-value", "0"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_dialog_plus_value_42", lambda: ["--sbx-dialog-plus-value", "42"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
VALUE_ERROR_CLI_CASES.append(("sbx_dialog_plus_value_100", lambda: ["--sbx-dialog-plus-value", "100"], MISSING_SBX_PROFILE_ERROR_MESSAGE))
# @formatter:on

@pytest.mark.parametrize(
    "case_name,args_list_factory,expected_error_snippet",
    ARGPARSE_ERROR_CLI_CASES,
    ids=[f"{i}__{case_name}__{'-'.join(args_list_factory())}" for i, (case_name, args_list_factory, _) in
         enumerate(ARGPARSE_ERROR_CLI_CASES)],
)
def test_argparse_error_cli_cases(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
        case_name: str,
        args_list_factory: ArgsListFactory,
        expected_error_snippet: str,
) -> None:
    # Generate CLI arguments
    args_list = args_list_factory()

    # Mock sys.argv to simulate CLI invocation
    monkeypatch.setattr(sys, "argv", ["g6-cli", "--dry-run", "--no-persist"] + args_list)

    # argparse validation should raise SystemExit (usually code 2)
    with pytest.raises(SystemExit) as exit_info:
        cli_main()
    assert exit_info.value.code == 2

    # Verify the error message contains the expected snippet
    captured = capsys.readouterr()
    assert expected_error_snippet in captured.err


@pytest.mark.parametrize(
    "case_name,args_list_factory,expected_error_snippet",
    VALUE_ERROR_CLI_CASES,
    ids=[f"{i}__{case_name}__{'-'.join(args_list_factory())}" for i, (case_name, args_list_factory, _) in
         enumerate(VALUE_ERROR_CLI_CASES)],
)
def test_value_error_cli_cases(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
        case_name: str,
        args_list_factory: ArgsListFactory,
        expected_error_snippet: str,
) -> None:
    # Generate CLI arguments
    args_list = args_list_factory()

    # Mock sys.argv to simulate CLI invocation
    monkeypatch.setattr(sys, "argv", ["g6-cli", "--dry-run", "--no-persist"] + args_list)

    # argparse validation should raise SystemExit (usually code 2)
    with pytest.raises(ValueError) as exit_info:
        cli_main()
    assert expected_error_snippet in str(exit_info.value)

    # Verify the error message contains the expected snippet
    captured = capsys.readouterr()
    assert expected_error_snippet in captured.err
