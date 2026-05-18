use clap::{Parser, Subcommand};

use crate::model::OutputMode;
use crate::model::sbx::ProfileName;
use crate::spec::{PlaybackFilter, SmartVolumeSpecial};
use crate::spec::decoder::DecoderMode;
use crate::spec::recording::MicEqPreset;

#[derive(Parser)]
#[command(name = "g6-cli", about = "SoundBlaster X G6 CLI (Windows, HID)", version)]
pub struct Cli {
    #[arg(long, global = true, help = "Print HID frames without sending them")]
    pub dry_run: bool,

    #[arg(long, global = true, help = "Print raw HID hex frames to stdout")]
    pub debug: bool,

    #[arg(long, global = true, help = "Do not read or write state.json")]
    pub no_persist: bool,

    #[command(subcommand)]
    pub command: Command,
}

#[derive(Subcommand)]
pub enum Command {
    /// Switch playback output between Speakers and Headphones
    Output {
        #[command(subcommand)]
        action: OutputAction,
    },
    /// Set the digital decoder mode
    Decoder {
        mode: DecoderMode,
    },
    /// Control device lighting
    Lighting {
        #[command(subcommand)]
        action: LightingAction,
    },
    /// Control HID playback settings
    Playback {
        #[command(subcommand)]
        action: PlaybackAction,
    },
    /// Control microphone settings
    Mic {
        #[command(subcommand)]
        action: MicAction,
    },
    /// Control SBX sound effects
    Sbx {
        #[command(subcommand)]
        action: SbxAction,
    },
}

// ── Output subcommands ────────────────────────────────────────────────────────

#[derive(Subcommand)]
pub enum OutputAction {
    /// Toggle between Speakers and Headphones
    Toggle,
    /// Set output to a specific mode
    Set { mode: OutputMode },
}

// ── Lighting subcommands ──────────────────────────────────────────────────────

#[derive(Subcommand)]
pub enum LightingAction {
    /// Disable device lighting
    Off,
    /// Enable lighting and set RGB colour
    Rgb {
        #[arg(value_name = "R", value_parser = clap::value_parser!(u8))]
        red: u8,
        #[arg(value_name = "G", value_parser = clap::value_parser!(u8))]
        green: u8,
        #[arg(value_name = "B", value_parser = clap::value_parser!(u8))]
        blue: u8,
    },
    /// Enable or disable the volume ring LED
    Ring {
        enable: OnOff,
    },
}

// ── Playback subcommands ──────────────────────────────────────────────────────

#[derive(Subcommand)]
pub enum PlaybackAction {
    /// Enable or disable Direct Mode
    Direct {
        enable: OnOff,
    },
    /// Enable or disable SPDIF-Out Direct Mode
    SpdifDirect {
        enable: OnOff,
    },
    /// Set the DAC playback filter
    Filter { filter: PlaybackFilter },
}

// ── Mic subcommands ───────────────────────────────────────────────────────────

#[derive(Subcommand)]
pub enum MicAction {
    /// Set mic boost (0, 10, 20, or 30 dB)
    Boost {
        #[arg(value_name = "dB", value_parser = parse_mic_boost_db)]
        db: u8,
    },
    /// Enable or disable noise reduction
    NoiseReduction {
        enable: OnOff,
        /// Noise reduction level (0, 20, 40, 60, 80, or 100)
        #[arg(long, value_name = "level", value_parser = parse_voice_clarity_level)]
        level: Option<u8>,
    },
    /// Enable or disable Acoustic Echo Cancellation
    Aec {
        enable: OnOff,
    },
    /// Enable or disable Smart Volume
    SmartVolume {
        enable: OnOff,
    },
    /// Enable or disable microphone equalizer
    Eq {
        enable: OnOff,
        /// Apply an EQ preset
        #[arg(long, value_name = "preset")]
        preset: Option<MicEqPreset>,
    },
}

// ── SBX subcommands ───────────────────────────────────────────────────────────

#[derive(Subcommand)]
pub enum SbxAction {
    /// Switch to a saved SBX profile (sends all stored settings to device)
    Switch { profile: ProfileName },
    /// Print the currently active SBX profile name
    Current,
    /// Control Surround effect
    Surround {
        profile: ProfileName,
        enable: OnOff,
        #[arg(long, value_parser = clap::value_parser!(u8).range(0..=100))]
        value: Option<u8>,
    },
    /// Control Crystalizer effect
    Crystalizer {
        profile: ProfileName,
        enable: OnOff,
        #[arg(long, value_parser = clap::value_parser!(u8).range(0..=100))]
        value: Option<u8>,
    },
    /// Control Bass effect
    Bass {
        profile: ProfileName,
        enable: OnOff,
        #[arg(long, value_parser = clap::value_parser!(u8).range(0..=100))]
        value: Option<u8>,
    },
    /// Control Smart Volume effect
    SmartVolume {
        profile: ProfileName,
        enable: OnOff,
        #[arg(long, value_parser = clap::value_parser!(u8).range(0..=100))]
        value: Option<u8>,
        /// Use Night or Loud special mode instead of a numeric value
        #[arg(long, conflicts_with = "value")]
        special: Option<SmartVolumeSpecial>,
    },
    /// Control Dialog Plus effect
    DialogPlus {
        profile: ProfileName,
        enable: OnOff,
        #[arg(long, value_parser = clap::value_parser!(u8).range(0..=100))]
        value: Option<u8>,
    },
}

// ── on/off value enum ─────────────────────────────────────────────────────────

#[derive(Clone, Copy, clap::ValueEnum)]
pub enum OnOff {
    On,
    Off,
}

impl From<OnOff> for bool {
    fn from(v: OnOff) -> bool {
        matches!(v, OnOff::On)
    }
}

// ── Custom parsers ────────────────────────────────────────────────────────────

fn parse_mic_boost_db(s: &str) -> Result<u8, String> {
    let db: u8 = s.parse().map_err(|_| format!("expected 0, 10, 20, or 30, got '{s}'"))?;
    if matches!(db, 0 | 10 | 20 | 30) {
        Ok(db)
    } else {
        Err(format!("mic boost must be 0, 10, 20, or 30 dB, got {db}"))
    }
}

fn parse_voice_clarity_level(s: &str) -> Result<u8, String> {
    let v: u8 = s.parse().map_err(|_| format!("expected 0, 20, 40, 60, 80, or 100, got '{s}'"))?;
    if matches!(v, 0 | 20 | 40 | 60 | 80 | 100) {
        Ok(v)
    } else {
        Err(format!("noise reduction level must be 0, 20, 40, 60, 80, or 100, got {v}"))
    }
}
