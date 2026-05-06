use super::{HidFrame, RECORDING_INTERMEDIATE, MODE_DATA, MODE_COMMIT, EMPTY_ADDITIONAL,
            mic_boost_bytes, voice_clarity_level_bytes, slider_percent_bytes};

// ── Mic boost ─────────────────────────────────────────────────────────────────

pub fn mic_boost(decibel: u8) -> Vec<HidFrame> {
    let value = mic_boost_bytes(decibel);
    vec![
        HidFrame::new([0x3c, 0x04], [0x00, 0x00], 0x02, value,   EMPTY_ADDITIONAL),
        HidFrame::new([0x3c, 0x02], [0x01, 0x00], 0x00, [0; 4],  EMPTY_ADDITIONAL),
    ]
}

// ── Voice clarity helpers ─────────────────────────────────────────────────────

fn toggle_recording_feature(audio_feature: u8, enable: bool) -> Vec<HidFrame> {
    let on_value  = slider_percent_bytes(100);
    let off_value = [0u8; 4];
    vec![
        HidFrame::recording(MODE_DATA,   audio_feature, if enable { on_value } else { off_value }),
        HidFrame::recording(MODE_COMMIT, audio_feature, off_value),
    ]
}

// ── Voice clarity features ────────────────────────────────────────────────────

pub fn voice_clarity_noise_reduction(enable: bool) -> Vec<HidFrame> {
    toggle_recording_feature(0x04, enable)
}

pub fn voice_clarity_noise_reduction_level(level: u8) -> Vec<HidFrame> {
    let value = voice_clarity_level_bytes(level);
    vec![
        HidFrame::recording(MODE_DATA,   0x05, value),
        HidFrame::recording(MODE_COMMIT, 0x05, [0; 4]),
    ]
}

pub fn voice_clarity_aec(enable: bool) -> Vec<HidFrame> {
    toggle_recording_feature(0x00, enable)
}

pub fn voice_clarity_smart_volume(enable: bool) -> Vec<HidFrame> {
    toggle_recording_feature(0x2C, enable)
}

pub fn voice_clarity_mic_eq(enable: bool) -> Vec<HidFrame> {
    toggle_recording_feature(0x13, enable)
}

pub fn voice_clarity_mic_eq_preset(preset: MicEqPreset) -> Vec<HidFrame> {
    let values = preset.feature_values();
    let features: [u8; 8] = [0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B];
    let mut frames = Vec::new();
    for (i, &feat) in features.iter().enumerate() {
        frames.push(HidFrame::recording(MODE_DATA,   feat, values[i]));
        frames.push(HidFrame::recording(MODE_COMMIT, feat, [0; 4]));
    }
    frames
}

// ── Mic EQ presets ────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Copy, PartialEq, clap::ValueEnum)]
pub enum MicEqPreset {
    Preset1,
    Preset2,
    Preset3,
    Preset4,
    Preset5,
    Preset6,
    Preset7,
    Preset8,
    Preset9,
    Preset10,
    PresetDm1,
}

impl MicEqPreset {
    // Returns [u8;4] values for features [0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B]
    fn feature_values(self) -> [[u8; 4]; 8] {
        match self {
            Self::Preset1  => [h("0000 40C0"), h("0000 80C0"), h("0000 0000"), h("0000 4000"), h("0000 4040"), h("0000 40C0"), h("0000 8040"), h("0000 A040")],
            Self::Preset2  => [h("0000 40C0"), h("0000 80C0"), h("0000 0000"), h("0000 4000"), h("0000 8040"), h("0000 00C0"), h("0000 0040"), h("0000 8040")],
            Self::Preset3  => [h("0000 00C0"), h("0000 40C0"), h("0000 4040"), h("0000 8040"), h("0000 8040"), h("0000 80C0"), h("0000 4040"), h("0000 0040")],
            Self::Preset4  => [h("0000 40C0"), h("0000 A0C0"), h("0000 0000"), h("0000 8040"), h("0000 0000"), h("0000 40C0"), h("0000 0000"), h("0000 0000")],
            Self::Preset5  => [h("0000 00C0"), h("0000 40C0"), h("0000 0040"), h("0000 8040"), h("0000 8040"), h("0000 0000"), h("0000 40C0"), h("0000 0040")],
            Self::Preset6  => [h("0000 A0C0"), h("0000 80C0"), h("0000 00C0"), h("0000 0000"), h("0000 4040"), h("0000 8040"), h("0000 C040"), h("0000 E040")],
            Self::Preset7  => [h("0000 0000"), h("0000 4040"), h("0000 00C0"), h("0000 80C0"), h("0000 80C0"), h("0000 00C0"), h("0000 A040"), h("0000 E040")],
            Self::Preset8  => [h("0000 0000"), h("0000 0000"), h("0000 0040"), h("0000 0040"), h("0000 4040"), h("0000 80C0"), h("0000 0040"), h("0000 8040")],
            Self::Preset9  => [h("0000 0000"), h("0000 0000"), h("0000 0040"), h("0000 0040"), h("0000 00C0"), h("0000 0000"), h("0000 80C0"), h("0000 8040")],
            Self::Preset10 => [h("0000 0000"), h("0000 0040"), h("0000 00C0"), h("0000 0000"), h("0000 4040"), h("0000 A040"), h("0000 C040"), h("0000 A040")],
            Self::PresetDm1=> [h("0000 0000"), h("0000 0041"), h("0000 0000"), h("0000 4041"), h("0000 4041"), h("0000 8040"), h("0000 0041"), h("0000 2041")],
        }
    }
}

/// Parse a spaced hex string like "0000 40C0" into a 4-byte array.
const fn h(s: &str) -> [u8; 4] {
    let b = s.as_bytes();
    // Filter spaces: collect non-space bytes as hex digits
    let mut hex = [0u8; 8];
    let mut hi = 0usize;
    let mut bi = 0usize;
    while bi < b.len() {
        if b[bi] != b' ' {
            hex[hi] = b[bi];
            hi += 1;
        }
        bi += 1;
    }
    [
        nibbles_to_byte(hex[0], hex[1]),
        nibbles_to_byte(hex[2], hex[3]),
        nibbles_to_byte(hex[4], hex[5]),
        nibbles_to_byte(hex[6], hex[7]),
    ]
}

const fn nibble(c: u8) -> u8 {
    match c {
        b'0'..=b'9' => c - b'0',
        b'a'..=b'f' => c - b'a' + 10,
        b'A'..=b'F' => c - b'A' + 10,
        _ => 0,
    }
}

const fn nibbles_to_byte(hi: u8, lo: u8) -> u8 {
    (nibble(hi) << 4) | nibble(lo)
}

