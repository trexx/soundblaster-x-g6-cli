mod api;
mod cli;
mod device;
mod model;
mod spec;
mod state;

use anyhow::Result;
use clap::Parser;

use crate::api::Api;
use crate::cli::{Cli, Command, LightingAction, MicAction, OutputAction, PlaybackAction, SbxAction};
use crate::device::G6;
use crate::spec::AudioFeature;

fn main() -> Result<()> {
    let cli = Cli::parse();

    let device = G6::open()?;
    let mut g6state = if cli.no_persist { crate::model::G6State::default() } else { state::load() };
    let mut api = Api::new(&device, &mut g6state, cli.debug, cli.dry_run, !cli.no_persist);

    match cli.command {
        Command::Output { action } => match action {
            OutputAction::Toggle      => api.output_toggle()?,
            OutputAction::Set { mode } => api.output_set(mode)?,
        },

        Command::Decoder { mode } => api.set_decoder_mode(mode)?,

        Command::Lighting { action } => match action {
            LightingAction::Off                   => api.lighting_off()?,
            LightingAction::Rgb { red, green, blue } => api.lighting_rgb(red, green, blue)?,
            LightingAction::Ring { enable }       => api.lighting_ring(enable.into())?,
        },

        Command::Playback { action } => match action {
            PlaybackAction::Direct { enable }      => api.playback_direct_mode(enable.into())?,
            PlaybackAction::SpdifDirect { enable } => api.playback_spdif_direct_mode(enable.into())?,
            PlaybackAction::Filter { filter }      => api.playback_filter(filter)?,
        },

        Command::Mic { action } => match action {
            MicAction::Boost { db } => api.mic_boost(db)?,
            MicAction::NoiseReduction { enable, level } => {
                api.mic_noise_reduction(enable.into())?;
                if let Some(l) = level {
                    api.mic_noise_reduction_level(l)?;
                }
            }
            MicAction::Aec { enable }         => api.mic_aec(enable.into())?,
            MicAction::SmartVolume { enable } => api.mic_smart_volume(enable.into())?,
            MicAction::Eq { enable, preset }  => {
                api.mic_eq(enable.into())?;
                if let Some(p) = preset {
                    api.mic_eq_preset(p)?;
                }
            }
        },

        Command::Sbx { action } => match action {
            SbxAction::Switch { profile } => api.sbx_switch(profile)?,
            SbxAction::Current            => println!("{}", api.sbx_current()),

            SbxAction::Surround { profile, enable, value } => {
                api.sbx_effect_toggle(profile, AudioFeature::SurroundToggle, enable.into())?;
                if let Some(v) = value {
                    api.sbx_effect_slider(profile, AudioFeature::SurroundSlider, v)?;
                }
            }
            SbxAction::Crystalizer { profile, enable, value } => {
                api.sbx_effect_toggle(profile, AudioFeature::CrystalizerToggle, enable.into())?;
                if let Some(v) = value {
                    api.sbx_effect_slider(profile, AudioFeature::CrystalizerSlider, v)?;
                }
            }
            SbxAction::Bass { profile, enable, value } => {
                api.sbx_effect_toggle(profile, AudioFeature::BassToggle, enable.into())?;
                if let Some(v) = value {
                    api.sbx_effect_slider(profile, AudioFeature::BassSlider, v)?;
                }
            }
            SbxAction::SmartVolume { profile, enable, value, special } => {
                api.sbx_effect_toggle(profile, AudioFeature::SmartVolumeToggle, enable.into())?;
                if let Some(s) = special {
                    api.sbx_smart_volume_special(profile, s)?;
                } else if let Some(v) = value {
                    api.sbx_effect_slider(profile, AudioFeature::SmartVolumeSlider, v)?;
                }
            }
            SbxAction::DialogPlus { profile, enable, value } => {
                api.sbx_effect_toggle(profile, AudioFeature::DialogPlusToggle, enable.into())?;
                if let Some(v) = value {
                    api.sbx_effect_slider(profile, AudioFeature::DialogPlusSlider, v)?;
                }
            }
        },
    }

    Ok(())
}
