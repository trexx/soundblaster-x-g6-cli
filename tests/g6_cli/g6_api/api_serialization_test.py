from __future__ import annotations

import os
import tempfile
from typing import Callable, Any, Generator

import pytest

import g6_cli.g6_api as g6_api
from g6_cli.g6_model import G6Model
from g6_cli.g6_model import Profile
from g6_cli.g6_model.playback import AudioMode
from g6_cli.g6_spec import (
    Channel,
    PlaybackFilter,
    SmartVolumeSpecialHex,
)
from g6_cli.g6_spec.decoder import DecoderMode
from g6_cli.g6_spec.recording import MicrophoneEqualizerPreset


@pytest.fixture
def temp_model_path() -> Generator[str, Any, None]:
    """Create a temporary file path for model JSON (deleted after test)."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        path = tmp.name
        yield path

        # cleanup temporary file
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass


@pytest.fixture
def api() -> g6_api.G6Api:
    """API instance with dry_run=True (no hardware communication)."""
    return g6_api.G6Api(dry_run=True, debug=False, persist_model=False)


# @formatter:off

# All test cases in one list — (component, getter, setter, values, short_name)
CASES = []

# ── Playback ────────────────────────────────────────────────────────────────
CASES.extend([
    ("playback", lambda m: m.get_mute(),                        lambda m, v: m.set_mute(v),                        [False, True],                          "mute"),
    ("playback", lambda m: m.get_is_speakers(),                 lambda m, v: m.set_is_speakers(v),                 [True, False],                          "is_speakers"),
    ("playback", lambda m: m.get_speakers_audio_mode(),         lambda m, v: m.set_speakers_audio_mode(v),         [AudioMode.AM_STEREO, AudioMode.AM_5_1], "speakers_audio_mode"),
    ("playback", lambda m: m.get_headphones_audio_mode(),         lambda m, v: m.set_headphones_audio_mode(v),     [AudioMode.AM_STEREO, AudioMode.AM_5_1], "headphones_audio_mode"),
    ("playback", lambda m: m.get_direct_mode_enabled(),         lambda m, v: m.set_direct_mode_enabled(v),         [False, True],                          "direct_mode"),
    ("playback", lambda m: m.get_spdif_out_direct_mode_enabled(), lambda m, v: m.set_spdif_out_direct_mode_enabled(v), [False, True],                     "spdif_out_direct"),
    ("playback", lambda m: m.get_filter(),                      lambda m, v: m.set_filter(v),                      list(PlaybackFilter),                   "filter"),
])

for ch in [Channel.CHANNEL_1, Channel.CHANNEL_2]:
    ch_label = "ch1" if ch == Channel.CHANNEL_1 else "ch2"
    CASES.append(
        ("playback", lambda m, _ch=ch: m.get_volume(_ch),         lambda m, v, _ch=ch: m.set_volume(v, {_ch}),         [0, 30, 70, 100],     f"volume_{ch_label}")
    )

# ── Decoder ─────────────────────────────────────────────────────────────────
CASES.append(
    ("decoder", lambda m: m.get_mode(),                         lambda m, v: m.set_mode(v),                        list(DecoderMode),                      "mode")
)

# ── Lighting ────────────────────────────────────────────────────────────────
CASES.extend([
    ("lighting", lambda m: m.get_enabled(),                     lambda m, v: m.set_enabled(v),                     [False, True],                          "enabled"),
    ("lighting", lambda m: m.get_rgb(),                         lambda m, v: m.set_rgb(*v),                        [(0,0,0), (128,64,255), (255,255,255)], "rgb"),
])

# ── Recording ───────────────────────────────────────────────────────────────
CASES.extend([
    ("recording", lambda m: m.get_mute(),                       lambda m, v: m.set_mute(v),                        [False, True],                          "mute"),
    ("recording", lambda m: m.get_mic_boost(),                  lambda m, v: m.set_mic_boost(v),                   [0, 10, 20, 30],                        "mic_boost"),
    ("recording", lambda m: m.get_mic_monitoring_mute(),        lambda m, v: m.set_mic_monitoring_mute(v),         [False, True],                          "mic_monitor_mute"),
    ("recording", lambda m: m.get_voice_clarity_noise_reduction_enabled(), lambda m, v: m.set_voice_clarity_noise_reduction_enabled(v), [False, True],     "vc_nr_enabled"),
    ("recording", lambda m: m.get_voice_clarity_noise_reduction_level(),
                                                                lambda m, v: m.set_voice_clarity_noise_reduction_level(v),
                                                                                                            [0, 20, 40, 60, 80, 100],   "vc_nr_level"),
    ("recording", lambda m: m.get_voice_clarity_acoustic_echo_cancellation_enabled(),
                                                                lambda m, v: m.set_voice_clarity_acoustic_echo_cancellation_enabled(v),
                                                                                                            [False, True],              "vc_aec"),
    ("recording", lambda m: m.get_voice_clarity_smart_volume_enabled(),
                                                                lambda m, v: m.set_voice_clarity_smart_volume_enabled(v),
                                                                                                            [False, True],              "vc_smart_vol"),
    ("recording", lambda m: m.get_voice_clarity_mic_equalizer_enabled(),
                                                                lambda m, v: m.set_voice_clarity_mic_equalizer_enabled(v),
                                                                                                            [False, True],              "vc_eq_enabled"),
    ("recording", lambda m: m.get_voice_clarity_mic_equalizer_preset(),
                                                                lambda m, v: m.set_voice_clarity_mic_equalizer_preset(v),
                                                                                                            list(MicrophoneEqualizerPreset), "vc_eq_preset"),
])

for ch in [Channel.CHANNEL_1, Channel.CHANNEL_2]:
    ch_label = "ch1" if ch == Channel.CHANNEL_1 else "ch2"
    CASES.extend([
        ("recording", lambda m, _ch=ch: m.get_mic_recording_volume(_ch),
                                  lambda m, v, _ch=ch: m.set_mic_recording_volume(v, {_ch}),          [0, 40, 80, 100],   f"mic_rec_vol_{ch_label}"),
        ("recording", lambda m, _ch=ch: m.get_mic_monitoring_volume(_ch),
                                  lambda m, v, _ch=ch: m.set_mic_monitoring_volume(v, {_ch}),         [0, 50, 90, 100],   f"mic_mon_vol_{ch_label}"),
    ])

# ── SBX ─────────────────────────────────────────────────────────────────────
CASES.extend([
    ("sbx", lambda m: m.get_surround_toggle(),                  lambda m, v: m.set_surround_toggle(v),             [False, True],                          "surround_toggle"),
    ("sbx", lambda m: m.get_surround_slider(),                  lambda m, v: m.set_surround_slider(v),             [0, 33, 66, 100],                       "surround_slider"),
    ("sbx", lambda m: m.get_crystalizer_toggle(),               lambda m, v: m.set_crystalizer_toggle(v),          [False, True],                          "crystalizer_toggle"),
    ("sbx", lambda m: m.get_crystalizer_slider(),               lambda m, v: m.set_crystalizer_slider(v),          [0, 25, 75, 100],                       "crystalizer_slider"),
    ("sbx", lambda m: m.get_bass_toggle(),                      lambda m, v: m.set_bass_toggle(v),                 [False, True],                          "bass_toggle"),
    ("sbx", lambda m: m.get_bass_slider(),                      lambda m, v: m.set_bass_slider(v),                 [0, 40, 80, 100],                       "bass_slider"),
    ("sbx", lambda m: m.get_smart_volume_toggle(),              lambda m, v: m.set_smart_volume_toggle(v),         [False, True],                          "smart_vol_toggle"),
    ("sbx", lambda m: m.get_smart_volume_slider(),              lambda m, v: m.set_smart_volume_slider(v),         [0, 50, 100],                           "smart_vol_slider"),
    ("sbx", lambda m: m.get_dialog_plus_toggle(),               lambda m, v: m.set_dialog_plus_toggle(v),          [False, True],                          "dialog_plus_toggle"),
    ("sbx", lambda m: m.get_dialog_plus_slider(),               lambda m, v: m.set_dialog_plus_slider(v),          [0, 60, 100],                           "dialog_plus_slider"),
    ("sbx", lambda m: m.get_smart_volume_special(),             lambda m, v: m.set_smart_volume_special(v),        list(SmartVolumeSpecialHex),            "smart_vol_special"),
])

# ── Mixer ───────────────────────────────────────────────────────────────────
CASES.extend([
    ("mixer", lambda m: m.get_playback_mute(),                  lambda m, v: m.set_playback_mute(v),                [False, True],                          "playback_mute"),
    ("mixer", lambda m: m.get_monitoring_line_in_mute(),        lambda m, v: m.set_monitoring_line_in_mute(v),     [False, True],                          "mon_line_in_mute"),
    ("mixer", lambda m: m.get_monitoring_external_mic_mute(),   lambda m, v: m.set_monitoring_external_mic_mute(v),  [False, True],                         "mon_ext_mic_mute"),
    ("mixer", lambda m: m.get_monitoring_spdif_in_mute(),       lambda m, v: m.set_monitoring_spdif_in_mute(v),    [False, True],                          "mon_spdif_in_mute"),
    ("mixer", lambda m: m.get_recording_line_in_mute(),         lambda m, v: m.set_recording_line_in_mute(v),      [False, True],                          "rec_line_in_mute"),
    ("mixer", lambda m: m.get_recording_external_mic_mute(),    lambda m, v: m.set_recording_external_mic_mute(v),   [False, True],                         "rec_ext_mic_mute"),
    ("mixer", lambda m: m.get_recording_spdif_in_mute(),        lambda m, v: m.set_recording_spdif_in_mute(v),     [False, True],                          "rec_spdif_in_mute"),
    ("mixer", lambda m: m.get_recording_what_u_hear_mute(),     lambda m, v: m.set_recording_what_u_hear_mute(v),  [False, True],                          "rec_what_u_hear_mute"),
])

for ch in [Channel.CHANNEL_1, Channel.CHANNEL_2]:
    ch_label = "ch1" if ch == Channel.CHANNEL_1 else "ch2"
    CASES.extend([
        ("mixer", lambda m, _ch=ch: m.get_monitoring_line_in_volume(_ch),
                                  lambda m, v, _ch=ch: m.set_monitoring_line_in_volume(v, {_ch}),     [0, 20, 60, 100],   f"mon_line_in_vol_{ch_label}"),
        ("mixer", lambda m, _ch=ch: m.get_monitoring_external_mic_volume(_ch),
                                  lambda m, v, _ch=ch: m.set_monitoring_external_mic_volume(v, {_ch}),[0, 30, 70, 100],   f"mon_ext_mic_vol_{ch_label}"),
        ("mixer", lambda m, _ch=ch: m.get_monitoring_spdif_in_volume(_ch),
                                  lambda m, v, _ch=ch: m.set_monitoring_spdif_in_volume(v, {_ch}),    [0, 40, 80, 100],   f"mon_spdif_in_vol_{ch_label}"),
        ("mixer", lambda m, _ch=ch: m.get_recording_line_in_volume(_ch),
                                  lambda m, v, _ch=ch: m.set_recording_line_in_volume(v, {_ch}),      [0, 50, 90, 100],   f"rec_line_in_vol_{ch_label}"),
        ("mixer", lambda m, _ch=ch: m.get_recording_external_mic_volume(_ch),
                                  lambda m, v, _ch=ch: m.set_recording_external_mic_volume(v, {_ch}), [0, 25, 75, 100],   f"rec_ext_mic_vol_{ch_label}"),
        ("mixer", lambda m, _ch=ch: m.get_recording_spdif_in_volume(_ch),
                                  lambda m, v, _ch=ch: m.set_recording_spdif_in_volume(v, {_ch}),     [0, 35, 85, 100],   f"rec_spdif_in_vol_{ch_label}"),
        ("mixer", lambda m, _ch=ch: m.get_recording_what_u_hear_volume(_ch),
                                  lambda m, v, _ch=ch: m.set_recording_what_u_hear_volume(v, {_ch}),  [0, 45, 95, 100],   f"rec_what_u_hear_vol_{ch_label}"),
    ])

# @formatter:on


@pytest.mark.parametrize(
    "component, getter, setter, values, name",
    CASES,
    ids=[f"{i}__{component}__{name}" for i, (component, getter, setter, values, name) in enumerate(CASES)]
)
def test_model_serialization_single_field(
        api: g6_api.G6Api,
        temp_model_path: str,
        component: str,
        getter: Callable,
        setter: Callable,
        values: list,
        name: str,  # not used in body, but helps with readability & debugging
) -> None:
    model = api.get_model()
    kwargs = {"profile_name" : Profile.Name.SPECIAL} if component == "sbx" else {}
    comp_obj = getattr(model, f"get_{component}")(**kwargs)

    # Default value round-trip
    default_value = getter(comp_obj)
    api.save_model(temp_model_path)

    loaded = G6Model.from_json(temp_model_path)
    loaded_comp = getattr(loaded, f"get_{component}")(**kwargs)
    assert getter(loaded_comp) == default_value

    # Changed value round-trip
    test_value = values[-1]
    if len(values) > 1 and test_value == default_value:
        test_value = values[1]

    setter(comp_obj, test_value)
    api.save_model(temp_model_path)

    loaded = G6Model.from_json(temp_model_path)
    loaded_comp = getattr(loaded, f"get_{component}")(**kwargs)
    assert getter(loaded_comp) == test_value


def test_full_model_roundtrip(api: g6_api.G6Api, temp_model_path: str) -> None:
    """
    Set a few distinct values across different components,
    save → load → compare the entire model state.
    """
    model = api.get_model()

    # Change a few representative values
    model.get_playback().set_mute(True)
    model.get_playback().set_volume(80, {Channel.CHANNEL_1, Channel.CHANNEL_2})
    model.get_decoder().set_mode(DecoderMode.FULL)
    model.get_lighting().set_rgb(100, 200, 50)
    model.get_recording().set_mic_boost(20)
    model.get_sbx(profile_name=Profile.Name.SPECIAL).set_surround_toggle(True)
    model.get_sbx(profile_name=Profile.Name.SPECIAL).set_surround_slider(75)
    model.get_mixer().set_monitoring_line_in_volume(60, {Channel.CHANNEL_1})

    # Save
    api.save_model(temp_model_path)

    # Load into fresh model
    loaded = G6Model.from_json(temp_model_path)

    # Compare dictionaries (simplest deep comparison)
    original_dict = model.to_dict()
    loaded_dict = loaded.to_dict()

    assert original_dict == loaded_dict, "Full model roundtrip failed — dictionaries differ"
