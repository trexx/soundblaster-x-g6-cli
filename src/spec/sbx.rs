use super::{HidFrame, AudioFeature, SmartVolumeSpecial, MODE_DATA, MODE_COMMIT, slider_percent_bytes};

pub fn sbx_toggle(feature: AudioFeature, enable: bool) -> Vec<HidFrame> {
    let value = if enable { slider_percent_bytes(100) } else { [0u8; 4] };
    vec![
        HidFrame::playback(MODE_DATA,   feature.byte(), value),
        HidFrame::playback(MODE_COMMIT, feature.byte(), [0; 4]),
    ]
}

pub fn sbx_slider(feature: AudioFeature, value: u8) -> Vec<HidFrame> {
    assert!(value <= 100, "slider value must be 0..=100");
    let vb = slider_percent_bytes(value);
    vec![
        HidFrame::playback(MODE_DATA,   feature.byte(), vb),
        HidFrame::playback(MODE_COMMIT, feature.byte(), [0; 4]),
    ]
}

pub fn sbx_smart_volume_special(special: SmartVolumeSpecial) -> Vec<HidFrame> {
    let af = AudioFeature::SmartVolumeSpecial.byte();
    let value = special.value_bytes();
    vec![
        HidFrame::playback(MODE_DATA,   af, value),
        HidFrame::playback(MODE_COMMIT, af, [0; 4]),
    ]
}
