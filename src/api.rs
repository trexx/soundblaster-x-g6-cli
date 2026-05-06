use anyhow::Result;

use crate::device::G6;
use crate::model::{G6State, OutputMode};
use crate::model::sbx::{ProfileName, SmartVolumeSpecialState};
use crate::spec::{AudioFeature, PlaybackFilter, SmartVolumeSpecial};
use crate::spec::decoder::{DecoderMode, decoder_mode};
use crate::spec::lighting::{lighting_disable, lighting_enable_set_rgb, lighting_volume_ring};
use crate::spec::playback::{
    enable_direct_mode, enable_spdif_out_direct_mode, playback_filter,
    toggle_to_headphones, toggle_to_speakers,
};
use crate::spec::recording::{
    MicEqPreset, mic_boost, voice_clarity_aec, voice_clarity_mic_eq, voice_clarity_mic_eq_preset,
    voice_clarity_noise_reduction, voice_clarity_noise_reduction_level, voice_clarity_smart_volume,
};
use crate::spec::sbx::{sbx_slider, sbx_smart_volume_special, sbx_toggle};

pub struct Api<'a> {
    device:  &'a G6,
    state:   &'a mut G6State,
    debug:   bool,
    dry_run: bool,
    persist: bool,
}

impl<'a> Api<'a> {
    pub fn new(device: &'a G6, state: &'a mut G6State, debug: bool, dry_run: bool, persist: bool) -> Self {
        Self { device, state, debug, dry_run, persist }
    }

    fn send(&self, frames: Vec<crate::spec::HidFrame>) -> Result<()> {
        self.device.send(&frames, self.debug, self.dry_run)
    }

    fn save(&mut self) -> Result<()> {
        if self.persist {
            crate::state::save(self.state)?;
        }
        Ok(())
    }

    // ── Output ────────────────────────────────────────────────────────────────

    pub fn output_toggle(&mut self) -> Result<()> {
        let next = match self.state.output {
            Some(OutputMode::Headphones) | None => OutputMode::Speakers,
            Some(OutputMode::Speakers)          => OutputMode::Headphones,
        };
        self.output_set(next)
    }

    pub fn output_set(&mut self, mode: OutputMode) -> Result<()> {
        let frames = match mode {
            OutputMode::Speakers   => toggle_to_speakers(),
            OutputMode::Headphones => toggle_to_headphones(),
        };
        self.send(frames)?;
        self.state.output = Some(mode);
        self.save()
    }

    // ── Decoder ───────────────────────────────────────────────────────────────

    pub fn set_decoder_mode(&self, mode: DecoderMode) -> Result<()> {
        self.send(decoder_mode(mode))
    }

    // ── Lighting ──────────────────────────────────────────────────────────────

    pub fn lighting_off(&self) -> Result<()> {
        self.send(lighting_disable())
    }

    pub fn lighting_rgb(&self, r: u8, g: u8, b: u8) -> Result<()> {
        self.send(lighting_enable_set_rgb(r, g, b))
    }

    pub fn lighting_ring(&self, enable: bool) -> Result<()> {
        self.send(lighting_volume_ring(enable))
    }

    // ── Playback ──────────────────────────────────────────────────────────────

    pub fn playback_direct_mode(&self, enable: bool) -> Result<()> {
        self.send(enable_direct_mode(enable))
    }

    pub fn playback_spdif_direct_mode(&self, enable: bool) -> Result<()> {
        self.send(enable_spdif_out_direct_mode(enable))
    }

    pub fn playback_filter(&self, filter: PlaybackFilter) -> Result<()> {
        self.send(playback_filter(filter))
    }

    // ── Mic ───────────────────────────────────────────────────────────────────

    pub fn mic_boost(&self, db: u8) -> Result<()> {
        self.send(mic_boost(db))
    }

    pub fn mic_noise_reduction(&self, enable: bool) -> Result<()> {
        self.send(voice_clarity_noise_reduction(enable))
    }

    pub fn mic_noise_reduction_level(&self, level: u8) -> Result<()> {
        self.send(voice_clarity_noise_reduction_level(level))
    }

    pub fn mic_aec(&self, enable: bool) -> Result<()> {
        self.send(voice_clarity_aec(enable))
    }

    pub fn mic_smart_volume(&self, enable: bool) -> Result<()> {
        self.send(voice_clarity_smart_volume(enable))
    }

    pub fn mic_eq(&self, enable: bool) -> Result<()> {
        self.send(voice_clarity_mic_eq(enable))
    }

    pub fn mic_eq_preset(&self, preset: MicEqPreset) -> Result<()> {
        self.send(voice_clarity_mic_eq_preset(preset))
    }

    // ── SBX ───────────────────────────────────────────────────────────────────

    pub fn sbx_current(&self) -> ProfileName {
        self.state.sbx.selected
    }

    pub fn sbx_switch(&mut self, profile: ProfileName) -> Result<()> {
        let p = self.state.sbx.profile(profile).clone();
        self.send(sbx_toggle(AudioFeature::SurroundToggle,    p.surround.toggle))?;
        self.send(sbx_slider(AudioFeature::SurroundSlider,    p.surround.slider))?;
        self.send(sbx_toggle(AudioFeature::CrystalizerToggle, p.crystalizer.toggle))?;
        self.send(sbx_slider(AudioFeature::CrystalizerSlider, p.crystalizer.slider))?;
        self.send(sbx_toggle(AudioFeature::BassToggle,        p.bass.toggle))?;
        self.send(sbx_slider(AudioFeature::BassSlider,        p.bass.slider))?;
        self.send(sbx_toggle(AudioFeature::SmartVolumeToggle, p.smart_volume.toggle))?;
        match &p.smart_volume.special {
            Some(sv) => self.send(sbx_smart_volume_special(sv.to_spec()))?,
            None      => self.send(sbx_slider(AudioFeature::SmartVolumeSlider, p.smart_volume.slider))?,
        }
        self.send(sbx_toggle(AudioFeature::DialogPlusToggle,  p.dialog_plus.toggle))?;
        self.send(sbx_slider(AudioFeature::DialogPlusSlider,  p.dialog_plus.slider))?;

        self.state.sbx.selected = profile;
        self.save()
    }

    pub fn sbx_effect_toggle(&mut self, profile: ProfileName, feature: AudioFeature, enable: bool) -> Result<()> {
        self.send(sbx_toggle(feature, enable))?;
        let p = self.state.sbx.profile_mut(profile);
        match feature {
            AudioFeature::SurroundToggle    => p.surround.toggle     = enable,
            AudioFeature::CrystalizerToggle => p.crystalizer.toggle  = enable,
            AudioFeature::BassToggle        => p.bass.toggle         = enable,
            AudioFeature::SmartVolumeToggle => p.smart_volume.toggle = enable,
            AudioFeature::DialogPlusToggle  => p.dialog_plus.toggle  = enable,
            _ => {}
        }
        self.save()
    }

    pub fn sbx_effect_slider(&mut self, profile: ProfileName, feature: AudioFeature, value: u8) -> Result<()> {
        self.send(sbx_slider(feature, value))?;
        let p = self.state.sbx.profile_mut(profile);
        match feature {
            AudioFeature::SurroundSlider    => p.surround.slider     = value,
            AudioFeature::CrystalizerSlider => p.crystalizer.slider  = value,
            AudioFeature::BassSlider        => p.bass.slider         = value,
            AudioFeature::SmartVolumeSlider => p.smart_volume.slider = value,
            AudioFeature::DialogPlusSlider  => p.dialog_plus.slider  = value,
            _ => {}
        }
        self.save()
    }

    pub fn sbx_smart_volume_special(&mut self, profile: ProfileName, special: SmartVolumeSpecial) -> Result<()> {
        self.send(sbx_smart_volume_special(special))?;
        let p = self.state.sbx.profile_mut(profile);
        p.smart_volume.special = Some(SmartVolumeSpecialState::from_spec(special));
        self.save()
    }
}
