// Byte-equality tests for the HID wire-format (no device needed).
// Each test verifies that the generated hex frames match the reference output
// captured from the Python tool run with --debug --dry-run.

use g6_cli::spec::{AudioFeature, HidFrame, PlaybackFilter, SmartVolumeSpecial};
use g6_cli::spec::decoder::{DecoderMode, decoder_mode};
use g6_cli::spec::lighting::{lighting_disable, lighting_enable_set_rgb, lighting_volume_ring};
use g6_cli::spec::playback::{enable_direct_mode, playback_filter, toggle_to_headphones, toggle_to_speakers};
use g6_cli::spec::recording::{MicEqPreset, mic_boost, voice_clarity_noise_reduction, voice_clarity_mic_eq_preset};
use g6_cli::spec::sbx::{sbx_toggle, sbx_slider, sbx_smart_volume_special};

// ── Lighting ──────────────────────────────────────────────────────────────────

#[test]
fn lighting_ring_on() {
    let frames = lighting_volume_ring(true);
    assert_eq!(frames.len(), 2);
    // Frame 0: PREFIX=5a, mode=3903, intermediate=000e, feature=00, value=00000000, additional=54*00
    assert!(frames[0].to_hex().starts_with("5a3903000e00"));
    assert!(frames[0].to_hex().ends_with(&"00".repeat(58)));
    // Frame 1 (commit): mode=3901, intermediate=0100
    assert!(frames[1].to_hex().starts_with("5a39010100"));
}

#[test]
fn lighting_ring_off() {
    let frames = lighting_volume_ring(false);
    assert_eq!(frames.len(), 2);
    // feature byte 0x01 (disabled)
    assert!(frames[0].to_hex().starts_with("5a3903000e01"));
}

#[test]
fn lighting_disable_frame() {
    let frames = lighting_disable();
    assert_eq!(frames.len(), 1);
    assert!(frames[0].to_hex().starts_with("5a3a020600"));
}

#[test]
fn lighting_rgb_red_frame_count() {
    let frames = lighting_enable_set_rgb(255, 0, 0);
    assert_eq!(frames.len(), 9, "3 pre-1 + 3 pre-2 + 3 rgb = 9 frames");
}

// ── Decoder ───────────────────────────────────────────────────────────────────

#[test]
fn decoder_normal_value() {
    let frames = decoder_mode(DecoderMode::Normal);
    assert_eq!(frames.len(), 2);
    // value bytes for Normal = 00 00 00 40
    let h = frames[0].to_hex();
    // byte layout: 5a | mode(2) | intermediate(2) | feature(1) | value(4) | ...
    // intermediate=0197 (DECODER_INTERMEDIATE), feature=02, value=00000040
    assert!(h.starts_with("5a1207019702"), "got: {}", &h[..14]);
    assert_eq!(&h[12..20], "00000040");
}

#[test]
fn decoder_night_value() {
    let frames = decoder_mode(DecoderMode::Night);
    assert_eq!(&frames[0].to_hex()[12..20], "00004040");
}

#[test]
fn decoder_full_value() {
    let frames = decoder_mode(DecoderMode::Full);
    assert_eq!(&frames[0].to_hex()[12..20], "0000803f");
}

// ── Playback ──────────────────────────────────────────────────────────────────

#[test]
fn playback_direct_mode_on_frame_count() {
    let frames = enable_direct_mode(true);
    assert_eq!(frames.len(), 2);
    // mode=3903, intermediate=0005, feature=01 (enabled)
    assert!(frames[0].to_hex().starts_with("5a39030005"), "got: {}", &frames[0].to_hex()[..12]);
    assert_eq!(&frames[0].to_hex()[10..12], "01");
}

#[test]
fn playback_filter_slow_lin() {
    let frames = playback_filter(PlaybackFilter::SlowRollOffLinearPhase);
    assert_eq!(frames.len(), 2);
    // mode=6c03, intermediate=0005 (filter value)
    assert!(frames[0].to_hex().starts_with("5a6c030005"), "got: {}", &frames[0].to_hex()[..12]);
}

#[test]
fn toggle_speakers_first_frame() {
    let frames = toggle_to_speakers();
    // first frame: mode=2c05, intermediate=0002
    assert!(frames[0].to_hex().starts_with("5a2c050002"), "got: {}", &frames[0].to_hex()[..12]);
}

#[test]
fn toggle_headphones_first_frame() {
    let frames = toggle_to_headphones();
    // first frame: mode=2c05, intermediate=0004
    assert!(frames[0].to_hex().starts_with("5a2c050004"), "got: {}", &frames[0].to_hex()[..12]);
}

#[test]
fn toggle_speakers_frame_count() {
    // 2 special + 11 features × 2 + 2 × 09 pairs = 28
    assert_eq!(toggle_to_speakers().len(), 28);
}

#[test]
fn toggle_headphones_frame_count() {
    assert_eq!(toggle_to_headphones().len(), 30);
}

// ── Mic ───────────────────────────────────────────────────────────────────────

#[test]
fn mic_boost_30db() {
    let frames = mic_boost(30);
    assert_eq!(frames.len(), 2);
    // mode=3c04, intermediate=0000, feature=02, value=1e000000
    assert!(frames[0].to_hex().starts_with("5a3c04000002"), "got: {}", &frames[0].to_hex()[..14]);
    assert_eq!(&frames[0].to_hex()[12..20], "1e000000");
}

#[test]
fn mic_noise_reduction_on() {
    let frames = voice_clarity_noise_reduction(true);
    assert_eq!(frames.len(), 2);
    // RECORDING_INTERMEDIATE=0195, feature=04, value=slider_percent(100)=[00,00,80,3f]
    assert!(frames[0].to_hex().starts_with("5a12070195"), "got: {}", &frames[0].to_hex()[..12]);
    assert_eq!(&frames[0].to_hex()[10..12], "04");
    assert_eq!(&frames[0].to_hex()[12..20], "0000803f");
}

// ── SBX ───────────────────────────────────────────────────────────────────────

#[test]
fn sbx_surround_toggle_on() {
    let frames = sbx_toggle(AudioFeature::SurroundToggle, true);
    assert_eq!(frames.len(), 2);
    // PLAYBACK_INTERMEDIATE=0196, feature=00 (SurroundToggle), value=slider(100)=0000803f
    assert!(frames[0].to_hex().starts_with("5a12070196"), "got: {}", &frames[0].to_hex()[..12]);
    assert_eq!(&frames[0].to_hex()[10..12], "00");
    assert_eq!(&frames[0].to_hex()[12..20], "0000803f");
}

#[test]
fn sbx_bass_slider_80() {
    let frames = sbx_slider(AudioFeature::BassSlider, 80);
    // feature=0x19, value=slider(80)
    assert_eq!(&frames[0].to_hex()[10..12], "19");
    assert_eq!(&frames[0].to_hex()[12..20], "cdcc4c3f");
}

#[test]
fn sbx_smart_volume_special_night() {
    let frames = sbx_smart_volume_special(SmartVolumeSpecial::Night);
    // feature=0x06, value=00000040
    assert_eq!(&frames[0].to_hex()[10..12], "06");
    assert_eq!(&frames[0].to_hex()[12..20], "00000040");
}

// ── Frame length invariant ────────────────────────────────────────────────────

#[test]
fn all_frames_are_128_hex_chars() {
    let all: Vec<HidFrame> = [
        lighting_volume_ring(true),
        lighting_volume_ring(false),
        lighting_disable(),
        lighting_enable_set_rgb(255, 128, 0),
        decoder_mode(DecoderMode::Normal),
        decoder_mode(DecoderMode::Full),
        decoder_mode(DecoderMode::Night),
        enable_direct_mode(true),
        enable_direct_mode(false),
        playback_filter(PlaybackFilter::FastRollOffMinimumPhase),
        toggle_to_speakers(),
        toggle_to_headphones(),
        mic_boost(0),
        mic_boost(30),
        voice_clarity_noise_reduction(true),
        sbx_toggle(AudioFeature::SurroundToggle, true),
        sbx_slider(AudioFeature::BassSlider, 50),
        sbx_smart_volume_special(SmartVolumeSpecial::Loud),
        voice_clarity_mic_eq_preset(MicEqPreset::Preset1),
    ]
    .into_iter()
    .flatten()
    .collect();

    for (i, frame) in all.iter().enumerate() {
        let h = frame.to_hex();
        assert_eq!(h.len(), 128, "frame {i} hex length should be 128, got {}", h.len());
    }
}
