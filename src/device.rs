use anyhow::{Context, Result};
use hidapi::{HidApi, HidDevice};

use crate::spec::HidFrame;

const G6_VENDOR_ID: u16  = 0x041e;
const G6_PRODUCT_ID: u16 = 0x3256;
const G6_HID_INTERFACE: i32 = 4;

pub struct G6 {
    device: HidDevice,
}

impl G6 {
    pub fn open() -> Result<Self> {
        let api = HidApi::new().context("Failed to initialize HID API")?;
        let info = api
            .device_list()
            .find(|d| {
                d.vendor_id() == G6_VENDOR_ID
                    && d.product_id() == G6_PRODUCT_ID
                    && d.interface_number() == G6_HID_INTERFACE
            })
            .with_context(|| {
                format!(
                    "SoundBlaster X G6 not found (VID={:#06x} PID={:#06x} interface={}).\n\
                     Is the device plugged in? Check Device Manager → Human Interface Devices.",
                    G6_VENDOR_ID, G6_PRODUCT_ID, G6_HID_INTERFACE
                )
            })?;

        let device = info.open_device(&api).context("Failed to open G6 HID interface")?;
        Ok(Self { device })
    }

    pub fn send(&self, frames: &[HidFrame], debug: bool, dry_run: bool) -> Result<()> {
        for frame in frames {
            let bytes = frame.to_bytes();

            if debug {
                println!("{}", frame.to_hex());
            }

            if dry_run {
                continue;
            }

            // Prepend report ID 0x00 (device uses no-ID protocol; hidapi requires it as byte 0)
            let mut buf = [0u8; 65];
            buf[1..].copy_from_slice(&bytes);
            self.device.write(&buf).context("HID write failed")?;

            // Drain any queued responses (non-blocking)
            let mut resp = [0u8; 64];
            loop {
                match self.device.read_timeout(&mut resp, 0) {
                    Ok(0) | Err(_) => break,
                    Ok(n) if debug => println!("Response({}): {:02x?}", n, &resp[..n]),
                    Ok(_) => {}
                }
            }
        }
        Ok(())
    }
}
