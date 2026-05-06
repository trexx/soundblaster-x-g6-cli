pub mod sbx;

use serde::{Deserialize, Serialize};

use crate::model::sbx::SbxState;

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize, clap::ValueEnum)]
#[serde(rename_all = "PascalCase")]
pub enum OutputMode {
    Speakers,
    Headphones,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct G6State {
    /// Last output toggle state so `output toggle` can alternate correctly.
    pub output: Option<OutputMode>,
    pub sbx:    SbxState,
}

impl Default for G6State {
    fn default() -> Self {
        Self {
            output: None,
            sbx:    SbxState::default(),
        }
    }
}
