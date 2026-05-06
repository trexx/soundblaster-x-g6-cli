use serde::{Deserialize, Serialize};

use crate::spec::SmartVolumeSpecial;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize, clap::ValueEnum)]
#[serde(rename_all = "PascalCase")]
pub enum ProfileName {
    Gaming,
    Music,
    Cinema,
    Special,
}

impl std::fmt::Display for ProfileName {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Gaming  => write!(f, "Gaming"),
            Self::Music   => write!(f, "Music"),
            Self::Cinema  => write!(f, "Cinema"),
            Self::Special => write!(f, "Special"),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SbxFeature {
    pub toggle: bool,
    pub slider: u8,
}

impl Default for SbxFeature {
    fn default() -> Self {
        Self { toggle: false, slider: 50 }
    }
}

/// Serializable version of SmartVolumeSpecial for the state JSON.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum SmartVolumeSpecialState {
    Night,
    Loud,
}

impl SmartVolumeSpecialState {
    pub fn to_spec(&self) -> SmartVolumeSpecial {
        match self {
            Self::Night => SmartVolumeSpecial::Night,
            Self::Loud  => SmartVolumeSpecial::Loud,
        }
    }

    pub fn from_spec(s: SmartVolumeSpecial) -> Self {
        match s {
            SmartVolumeSpecial::Night => Self::Night,
            SmartVolumeSpecial::Loud  => Self::Loud,
        }
    }
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct SmartVolumeFeature {
    pub toggle: bool,
    pub slider: u8,
    pub special: Option<SmartVolumeSpecialState>,
}

impl SmartVolumeFeature {
    fn default_state() -> Self {
        Self { toggle: false, slider: 50, special: None }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SbxProfile {
    pub surround:     SbxFeature,
    pub crystalizer:  SbxFeature,
    pub bass:         SbxFeature,
    pub smart_volume: SmartVolumeFeature,
    pub dialog_plus:  SbxFeature,
}

impl Default for SbxProfile {
    fn default() -> Self {
        Self {
            surround:     SbxFeature::default(),
            crystalizer:  SbxFeature::default(),
            bass:         SbxFeature::default(),
            smart_volume: SmartVolumeFeature::default_state(),
            dialog_plus:  SbxFeature::default(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SbxState {
    pub selected: ProfileName,
    pub gaming:   SbxProfile,
    pub music:    SbxProfile,
    pub cinema:   SbxProfile,
    pub special:  SbxProfile,
}

impl Default for SbxState {
    fn default() -> Self {
        Self {
            selected: ProfileName::Gaming,
            gaming:   SbxProfile::default(),
            music:    SbxProfile::default(),
            cinema:   SbxProfile::default(),
            special:  SbxProfile::default(),
        }
    }
}

impl SbxState {
    pub fn profile_mut(&mut self, name: ProfileName) -> &mut SbxProfile {
        match name {
            ProfileName::Gaming  => &mut self.gaming,
            ProfileName::Music   => &mut self.music,
            ProfileName::Cinema  => &mut self.cinema,
            ProfileName::Special => &mut self.special,
        }
    }

    pub fn profile(&self, name: ProfileName) -> &SbxProfile {
        match name {
            ProfileName::Gaming  => &self.gaming,
            ProfileName::Music   => &self.music,
            ProfileName::Cinema  => &self.cinema,
            ProfileName::Special => &self.special,
        }
    }
}
