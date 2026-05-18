use super::{HidFrame, PlaybackFilter, MODE_DATA, MODE_COMMIT, EMPTY_ADDITIONAL};

pub fn toggle_to_speakers() -> Vec<HidFrame> {
    let mut frames = vec![
        HidFrame::new([0x2c, 0x05], [0x00, 0x02], 0x00, [0; 4], EMPTY_ADDITIONAL),
        HidFrame::new([0x2c, 0x01], [0x01, 0x00], 0x00, [0; 4], EMPTY_ADDITIONAL),
    ];
    for feat in [0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14] {
        frames.push(HidFrame::playback(MODE_DATA,   feat, [0; 4]));
        frames.push(HidFrame::playback(MODE_COMMIT, feat, [0; 4]));
    }
    frames.push(HidFrame::playback(MODE_DATA,   0x09, [0; 4]));
    frames.push(HidFrame::playback(MODE_COMMIT, 0x09, [0; 4]));
    frames.push(HidFrame::playback(MODE_DATA,   0x09, [0; 4]));
    frames.push(HidFrame::playback(MODE_COMMIT, 0x09, [0; 4]));
    frames
}

pub fn toggle_to_headphones() -> Vec<HidFrame> {
    let mut frames = vec![
        HidFrame::new([0x2c, 0x05], [0x00, 0x04], 0x00, [0; 4], EMPTY_ADDITIONAL),
        HidFrame::new([0x2c, 0x01], [0x01, 0x00], 0x00, [0; 4], EMPTY_ADDITIONAL),
    ];
    for feat in [0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14] {
        frames.push(HidFrame::playback(MODE_DATA,   feat, [0; 4]));
        frames.push(HidFrame::playback(MODE_COMMIT, feat, [0; 4]));
    }
    frames.push(HidFrame::playback(MODE_DATA,   0x09, [0; 4]));
    frames.push(HidFrame::playback(MODE_COMMIT, 0x09, [0; 4]));
    frames.push(HidFrame::playback(MODE_DATA,   0x06, [0; 4]));
    frames.push(HidFrame::playback(MODE_COMMIT, 0x06, [0; 4]));
    frames.push(HidFrame::playback(MODE_DATA,   0x09, [0; 4]));
    frames.push(HidFrame::playback(MODE_COMMIT, 0x09, [0; 4]));
    frames
}

pub fn enable_direct_mode(enable: bool) -> Vec<HidFrame> {
    let af = if enable { 0x01 } else { 0x00 };
    vec![
        HidFrame::new([0x39, 0x03], [0x00, 0x05], af, [0; 4], EMPTY_ADDITIONAL),
        HidFrame::new([0x39, 0x01], [0x01, 0x00], 0x00, [0; 4], EMPTY_ADDITIONAL),
    ]
}

pub fn enable_spdif_out_direct_mode(enable: bool) -> Vec<HidFrame> {
    let af = if enable { 0x01 } else { 0x00 };
    vec![
        HidFrame::new([0x39, 0x03], [0x00, 0x0d], af, [0; 4], EMPTY_ADDITIONAL),
        HidFrame::new([0x39, 0x01], [0x01, 0x00], 0x00, [0; 4], EMPTY_ADDITIONAL),
    ]
}

pub fn playback_filter(filter: PlaybackFilter) -> Vec<HidFrame> {
    let intermediate = filter.intermediate_bytes();
    vec![
        HidFrame::new([0x6c, 0x03], intermediate, 0x00, [0; 4], EMPTY_ADDITIONAL),
        HidFrame::new([0x6c, 0x01], [0x01, 0x00], 0x00, [0; 4], EMPTY_ADDITIONAL),
    ]
}

