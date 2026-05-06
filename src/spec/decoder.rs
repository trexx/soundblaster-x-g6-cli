use super::{HidFrame, MODE_DATA, MODE_COMMIT};

const DECODER_AUDIO_FEATURE: u8 = 0x02;

#[derive(Debug, Clone, Copy, PartialEq, clap::ValueEnum)]
pub enum DecoderMode {
    Normal,
    Full,
    Night,
}

impl DecoderMode {
    fn value_bytes(self) -> [u8; 4] {
        match self {
            Self::Normal => [0x00, 0x00, 0x00, 0x40],
            Self::Full   => [0x00, 0x00, 0x80, 0x3f],
            Self::Night  => [0x00, 0x00, 0x40, 0x40],
        }
    }
}

pub fn decoder_mode(mode: DecoderMode) -> Vec<HidFrame> {
    vec![
        HidFrame::decoder(MODE_DATA,   DECODER_AUDIO_FEATURE, mode.value_bytes()),
        HidFrame::decoder(MODE_COMMIT, DECODER_AUDIO_FEATURE, [0; 4]),
    ]
}
