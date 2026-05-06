# SoundBlaster X G6 CLI

A Windows CLI tool for controlling the Creative SoundBlaster X G6 USB DAC.

Communicates via the HID interface (USB interface 4) — no driver replacement required.
The device's audio class driver continues to function normally during use.

---

## Requirements

- Windows 10 or later (x64)
- SoundBlaster X G6 connected via USB

---

## Installation

Download `g6-cli.exe` from the Releases page and place it anywhere on your `PATH`.
`state.json` is created automatically next to the executable on first run.

### Build from source

```
cargo build --release --target x86_64-pc-windows-msvc
```

The binary will be at `target\x86_64-pc-windows-msvc\release\g6-cli.exe`.

---

## Usage

```
g6-cli [OPTIONS] <COMMAND>
```

### Global options

| Flag | Description |
|---|---|
| `--dry-run` | Print what would be sent without writing to the device |
| `--debug` | Print raw HID hex frames to stdout |
| `--no-persist` | Do not read or write `state.json` |

---

## Commands

### Output

```
g6-cli output toggle
g6-cli output set <speakers|headphones>
```

`toggle` alternates between Speakers and Headphones using the last state saved in `state.json`.

---

### Decoder

```
g6-cli decoder <normal|full|night>
```

---

### Lighting

```
g6-cli lighting off
g6-cli lighting rgb <R> <G> <B>       # R/G/B: 0-255
g6-cli lighting ring <on|off>          # volume-knob LED
```

---

### Playback

```
g6-cli playback direct <on|off>
g6-cli playback spdif-direct <on|off>
g6-cli playback filter <fast-min|slow-min|fast-lin|slow-lin>
```

---

### Mic

```
g6-cli mic boost <0|10|20|30>
g6-cli mic noise-reduction <on|off> [--level <0|20|40|60|80|100>]
g6-cli mic aec <on|off>
g6-cli mic smart-volume <on|off>
g6-cli mic eq <on|off> [--preset <preset-1|...|preset-dm-1>]
```

Mic EQ presets: `preset-1` through `preset-10` and `preset-dm-1`.

---

### SBX Sound Effects

Profiles: `gaming` | `music` | `cinema` | `special`

```
g6-cli sbx switch <profile>      # apply stored settings for this profile
g6-cli sbx current               # print active profile name

g6-cli sbx <profile> surround    <on|off> [--value 0-100]
g6-cli sbx <profile> crystalizer <on|off> [--value 0-100]
g6-cli sbx <profile> bass        <on|off> [--value 0-100]
g6-cli sbx <profile> smart-volume <on|off> [--value 0-100 | --special <night|loud>]
g6-cli sbx <profile> dialog-plus <on|off> [--value 0-100]
```

Settings are persisted per-profile in `state.json` so `sbx switch` replays them next time.

---

## Notes

- Volume, mute, and mixer controls are handled by Windows' own audio stack (right-click the
  taskbar volume icon -> "Open Volume Mixer"). Those features required exclusive access to the
  USB AudioControl interface, which would disable system audio.
- `state.json` sits next to `g6-cli.exe`. Keep them together, or use `--no-persist` to skip it.
