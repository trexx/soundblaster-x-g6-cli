use std::path::PathBuf;

use anyhow::Result;

use crate::model::G6State;

fn state_path() -> PathBuf {
    std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|d| d.join("state.json")))
        .unwrap_or_else(|| PathBuf::from("state.json"))
}

pub fn load() -> G6State {
    let path = state_path();
    if !path.exists() {
        return G6State::default();
    }
    match std::fs::read_to_string(&path).and_then(|s| {
        serde_json::from_str(&s).map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))
    }) {
        Ok(state) => state,
        Err(e) => {
            eprintln!("Warning: could not load state.json ({}); using defaults.", e);
            G6State::default()
        }
    }
}

pub fn save(state: &G6State) -> Result<()> {
    let path = state_path();
    let json = serde_json::to_string_pretty(state)?;
    std::fs::write(path, json)?;
    Ok(())
}
